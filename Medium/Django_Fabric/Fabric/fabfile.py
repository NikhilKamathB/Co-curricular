import os
from dotenv import load_dotenv
from fabric.tasks import task
from fabric import Connection
load_dotenv()

LOCAL = os.getenv("LOCAL")
USER = os.getenv("USER_NAME")
HOST = os.getenv("HOST")
PROJECT = os.getenv("PROJECT")
SSH_FILE = os.getenv("SSH_FILE")
GIT_REPO = os.getenv("GIT_REPO")
GITHUB_KEY_PATH = os.getenv("GITHUB_KEY_PATH")
GITHUB_KEY_NAME = GITHUB_KEY_PATH.split('/')[-1]
PROJECT_DJANGO_ROOT = os.getenv("PROJECT_DJANGO_ROOT")
PROJECT_DJANGO_WSGI_APP = os.getenv("PROJECT_DJANGO_WSGI_APP")
SERVER_URL = os.getenv('SERVER_URL')

LOCAL_USER = os.getenv("LOCAL_USER_NAME")
PASSWORD = os.getenv("PASSWORD")
LOCAL_HOST = os.getenv("LOCAL_HOST")

CONNECT_KWARGS = {"key_filename":[SSH_FILE]} if LOCAL == 'false' else {"password": PASSWORD}
_USER = USER if LOCAL == 'false' else LOCAL_USER
_HOST = HOST if LOCAL == 'false' else LOCAL_HOST
CONN = Connection(host=_HOST, user=_USER, connect_kwargs=CONNECT_KWARGS)

@task
def demo(ctx, folder):
    with CONN.cd(f"{folder}"):
        CONN.run(f'''cat > temp.txt << EOF
This is a demo text file.
It will be deleted after running this fab function.
EOF
''')
        CONN.run("cat temp.txt")
        CONN.run("wc -c temp.txt")
        CONN.run("rm -rf temp.txt")


# Misc actions.
@task 
def ls(ctx, folder):
    CONN.run(f"ls {folder}")

@task 
def cat(ctx, folder, file):
    with CONN.cd(folder):
        CONN.run(f"cat {file}")

@task
def mv(ctx, src, dest):
    CONN.run(f"mv {src} {dest}")

@task
def mkdir(ctx, path):
    CONN.run(f"mkdir {path} -p")

@task
def touch(ctx, file):
    CONN.run(f"touch {file}")

@task
def rm(ctx, path):
    CONN.run(f"rm -rf {path}")

# System setup.
@task
def apt_update(ctx):
    CONN.sudo("apt-get update -y")

@task
def install_nginx(ctx):
    CONN.sudo("apt install nginx -y")

@task
def install_virtualenv(ctx):
    CONN.sudo("apt-get install python3-pip -y")
    CONN.run("python3 -m pip install virtualenv")

# Application specific.
@task
def create_venv(ctx):
    with CONN.cd(f"~/{PROJECT}"):
        CONN.run("python3 -m virtualenv venv")

# Git related actions (Before running these functions, deploy keys for your repo).
# Copy private key -> set git congif file -> clone -> fetch (later).
@task
def copy_key_file(ctx):
    ctx.run(f"rsync -e 'ssh -i {SSH_FILE}' {GITHUB_KEY_PATH} ubuntu@{HOST}:~/.ssh")
    ctx.run(f"rsync -e 'ssh -i {SSH_FILE}' {GITHUB_KEY_PATH}.pub ubuntu@{HOST}:~/.ssh")
    
@task
def git_config(ctx):
    with CONN.cd("~/.ssh/"):
        CONN.run(f'''cat > config << EOF
Host github.com-repo-django-fabric
  Preferredauthentications publickey
  IdentityFile=/home/{USER}/.ssh/{GITHUB_KEY_NAME}
AddKeysToAgent yes
EOF
''')
    # CONN.run(f"yes | ssh -T git@github.com")
    # CONN.run(f'ssh-keyscan -H github.com >> ~/.ssh/known_hosts && eval "$(ssh-agent -s)" && ssh-add ~/.ssh/{GITHUB_KEY_NAME}')

@task
def git_clone(ctx):
    CONN.run(f'ssh-keyscan -H github.com >> ~/.ssh/known_hosts')
    CONN.run(f'eval "$(ssh-agent -s)" && ssh-add ~/.ssh/{GITHUB_KEY_NAME} && git clone {GIT_REPO}')

@task
def git_fetch(ctx, path=None, branch='master'):
    path = f"~/{PROJECT}/{PROJECT_DJANGO_ROOT}" if path is None else path
    with CONN.cd(path):
        CONN.run("git fetch --all")
        CONN.run(f"git checkout -f origin/{branch}")

@task
def install_requirements(ctx):
    with CONN.cd(f"~/{PROJECT}/"):
        CONN.run("source venv/bin/activate && pip install -r requirements.txt")

# Gunicorn setup.
@task
def setup_gunicorn(ctx):
    CONN.run(f'''cat > {PROJECT}.socket << EOF
[Unit]
Description={PROJECT} socket

[Socket]
ListenStream=/run/{PROJECT}.sock
SocketUser=www-data

[Install]
WantedBy=sockets.target
EOF
''')
    CONN.sudo(f'''cat > {PROJECT}.service << EOF
[Unit]
Description={PROJECT} daemon
Requires={PROJECT}.socket
After=network.target

[Service]
Type=notify
User={USER}
Group={USER}
RuntimeDirectory=gunicorn
WorkingDirectory=/home/{USER}/{PROJECT}
ExecStart=/home/{USER}/{PROJECT}/venv/bin/gunicorn {PROJECT_DJANGO_WSGI_APP}.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
''')
    CONN.sudo(f"mv {PROJECT}.socket /etc/systemd/system/")
    CONN.sudo(f"mv {PROJECT}.service /etc/systemd/system/")
    CONN.sudo("systemctl daemon-reload")
    CONN.sudo(f"systemctl enable --now {PROJECT}.socket")
    CONN.sudo(f"systemctl start {PROJECT}.service")

# Nginx setup.
@task
def setup_nginx(ctx):
    CONN.sudo("rm -f /etc/nginx/sites-enabled/default")
    CONN.run(f'''cat > {PROJECT}.conf << EOF
upstream {PROJECT}_server {{
    server unix:/run/{PROJECT}.sock fail_timeout=0;
  }}
server {{
    listen 80 default_server;
    server_name {SERVER_URL};

    client_max_body_size 4G;

    access_log /var/log/nginx/{PROJECT}-access.log;
    error_log /var/log/nginx/{PROJECT}-error.log;

    keepalive_timeout 5;

    location @proxy_to_app {{
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header Host \$http_host;
      proxy_redirect off;
      proxy_pass http://{PROJECT}_server;
    }}
}}
EOF
''')
    CONN.sudo(f"mv {PROJECT}.conf /etc/nginx/sites-enabled/")
    CONN.sudo("nginx -t")
    CONN.sudo("systemctl restart nginx")

@task
def restart_nginx(ctx):
    CONN.sudo("systemctl restart nginx")

@task
def test_server(ctx):
    ctx.run(f"curl -i {HOST}")

@task
def test_gunicorn_service(ctx):
    CONN.sudo(f"curl --unix-socket /run/{PROJECT}.sock http", user="www-data")