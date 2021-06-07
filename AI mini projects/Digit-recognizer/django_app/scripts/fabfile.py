import os
from dotenv import load_dotenv
from fabric.tasks import task
from fabric import Connection
from invoke import run as local
load_dotenv()

USER = "nikhilkb98"
SERVER = os.getenv("SERVER")
PROJECT = os.getenv("PROJECT")
PROJECT_DJANGO_ROOT = os.getenv("PROJECT_DJANGO_ROOT")
PROJECT_DJANGO_WSGI_APP = os.getenv("PROJECT_DJANGO_WSGI_APP")
SSH_FILE = os.getenv("SSH_FILE")
GIT_REPO = os.getenv("GIT_REPO")
SERVER_NAME = os.getenv("SERVER_NAME")
PROJECT_STATIC_ROOT = os.getenv("PROJECT_STATIC_ROOT")

CONNECT_KWARGS = {"key_filename":[SSH_FILE]}
c = Connection(host=SERVER, user=USER, connect_kwargs=CONNECT_KWARGS)
print(f"Connected to SERVER={SERVER} user={USER}")
print(f'''
USER = {USER}
SERVER = {SERVER}
PROJECT = {PROJECT}
PROJECT_DJANGO_ROOT = {PROJECT_DJANGO_ROOT}
PROJECT_DJANGO_WSGI_APP = {PROJECT_DJANGO_WSGI_APP}
SSH_FILE = {SSH_FILE}
GIT_REPO = {GIT_REPO}
SERVER_NAME = {SERVER_NAME}
PROJECT_STATIC_ROOT = {PROJECT_STATIC_ROOT}
''')

"""
This script will install and configure a django app in the destination server.
The daemon is spawned using systemd.
"""

@task 
def ls(ctx, folder):
    c.run(f"ls -lrta {folder}")

@task 
def rm(ctx, folder):
    c.run(f"rm -rf {folder}")

@task 
def cat(ctx, file):
    c.run(f"cat {file}")

@task
def apt_update(ctx):
    c.sudo("apt-get update -y")

@task
def install_nginx(ctx):
    c.sudo("apt install nginx -y")

@task
def install_git(ctx):
    c.sudo("apt install git-all -y")

@task
def git_clone(ctx):
    print(f"git clone {GIT_REPO} {PROJECT}")
    with c.cd(f"~/"):
        print(f"rm -rf {PROJECT}")
        c.run(f"rm -rf {PROJECT}")
        c.run(f"git clone {GIT_REPO} {PROJECT}", pty=True)

@task 
def git_pull(ctx):
    with c.cd(f"~/{PROJECT}"):
        c.run(f"git pull")

@task
def install_virtualenv(ctx):
    c.sudo("apt-get install python3-pip -y")
    c.run("python3 -m pip install virtualenv")

@task
def create_venv(ctx):
    with c.cd(f"~/{PROJECT}/"):
        c.run("python3 -m virtualenv venv")

@task
def install_requirements(ctx):
    with c.cd(f"~/{PROJECT}/"):
        c.run("source venv/bin/activate")
        with c.cd(f"~/{PROJECT}/{PROJECT_DJANGO_ROOT}/"):
            c.run(f"~/{PROJECT}/venv/bin/pip install -r requirements.txt")

@task
def create_gunicorn_service(ctx):
    c.run(f'''cat > {PROJECT}.socket << EOF
[Unit]
Description={PROJECT} socket
[Socket]
ListenStream=/run/{PROJECT}.sock
SocketUser=www-data
[Install]
WantedBy=sockets.target
EOF
''')
    print("created socket file")
    c.sudo(f'''cat > {PROJECT}.service << EOF
[Unit]
Description={PROJECT} daemon
Requires={PROJECT}.socket
After=network.target

[Service]
Type=notify
User={USER}
Group={USER}
RuntimeDirectory=gunicorn
WorkingDirectory=/home/{USER}/{PROJECT}/{PROJECT_DJANGO_ROOT}
ExecStart=/home/{USER}/{PROJECT}/venv/bin/gunicorn {PROJECT_DJANGO_WSGI_APP}.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
''')
    print("created service file")
    c.sudo(f"mv {PROJECT}.socket /etc/systemd/system/")
    c.sudo(f"mv {PROJECT}.service /etc/systemd/system/")
    c.sudo("systemctl daemon-reload")
    c.sudo(f"systemctl enable --now {PROJECT}.socket")
    c.sudo(f"systemctl start {PROJECT}.service")

@task
def test_gunicorn_service(ctx):
    c.sudo(f"curl --unix-socket /run/{PROJECT}.sock http", user="www-data")

@task
def create_nginx_site(ctx):
    c.sudo("rm -f /etc/nginx/sites-enabled/default")
    c.sudo(f"rm -f {PROJECT}.conf")
    c.run(f'''cat > {PROJECT}.conf << EOF
upstream {PROJECT}_server {{
  server unix:/run/{PROJECT}.sock fail_timeout=0;
}}

server {{
    listen 80;
    listen 443;
    server_name {SERVER_NAME};

    client_max_body_size 4G;

    access_log /var/log/nginx/{PROJECT}-access.log;
    error_log /var/log/nginx/{PROJECT}-error.log;

    keepalive_timeout 5;

    # path for static files
    root /home/{USER}/{PROJECT}/{PROJECT_DJANGO_ROOT}/dist;

    location / {{
      # checks for static file, if not found proxy to app
      try_files \$uri @proxy_to_{PROJECT};
    }}


    location @proxy_to_{PROJECT} {{
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto \$scheme;
      proxy_set_header Host \$http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://{PROJECT}_server;
    }}

    error_page 500 502 503 504 /500.html;
    location = /500.html {{
	    root /home/{USER}/{PROJECT}/{PROJECT_DJANGO_ROOT}/{PROJECT_STATIC_ROOT}/500.html;
    }}
}}
EOF
''')
    c.sudo(f"rm -f /etc/nginx/sites-enabled/{PROJECT}.conf")
    c.sudo(f"mv {PROJECT}.conf /etc/nginx/sites-enabled/")
    c.sudo(f"nginx -t")
    c.sudo("systemctl restart nginx")


@task 
def put_env(ctx, PROD_ENV_FILE):
    """the parameter file will be copied as .env and service is relaunched"""
    basefile = os.path.basename(PROD_ENV_FILE)
    local(f"rsync -e 'ssh -i {SSH_FILE}' {PROD_ENV_FILE} ubuntu@{SERVER}:~/{PROJECT}/{PROJECT_DJANGO_ROOT}/")
    if basefile != ".env":#rename to .env
        c.run(f"mv ~/{PROJECT}/{PROJECT_DJANGO_ROOT}/{basefile} ~/{PROJECT}/{PROJECT_DJANGO_ROOT}/.env")

@task
def deploy(ctx, branch="master"):
    with c.cd(f"~/{PROJECT}/"):
        c.run("git fetch --all")
        c.run(f"git checkout -f origin/{branch}")
        c.run("source venv/bin/activate")
        with c.cd(f"~/{PROJECT}/{PROJECT_DJANGO_ROOT}/"):
            c.run(f"~/{PROJECT}/venv/bin/pip install -r requirements.txt")
            c.run(f"~/{PROJECT}/venv/bin/python manage.py migrate")
            c.run(f"~/{PROJECT}/venv/bin/python manage.py collectstatic")
    c.sudo(f"systemctl restart {PROJECT}.service")