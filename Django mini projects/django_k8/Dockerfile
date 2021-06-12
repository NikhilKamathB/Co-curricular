# using ubuntu for our image
FROM ubuntu:latest
LABEL name="djangok8"
LABEL version="latest"

# updating ubuntu packages
RUN apt-get update && yes|apt-get upgrade

# installing necessary libs
RUN apt-get install -y sudo python3-pip
RUN python3 -m pip install virtualenv

# adding user ubuntu with no password, add to sudo group and setting working directory
RUN adduser --disabled-password --gecos '' ubuntu
RUN adduser ubuntu sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ubuntu
WORKDIR /home/ubuntu/
RUN chmod a+rwx /home/ubuntu/

# creating venv
RUN python3 -m virtualenv venv
ENV PATH venv/bin:$PATH

# setting project and environment
RUN mkdir /home/ubuntu/app
ADD . /home/ubuntu/app
RUN venv/bin/pip install --upgrade pip && venv/bin/pip install -r app/requirements.txt
WORKDIR /home/ubuntu/app
EXPOSE 8000
CMD /home/ubuntu/venv/bin/gunicorn -b :8000 django_k8.wsgi