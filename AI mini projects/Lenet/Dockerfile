# using ubuntu for our image
FROM ubuntu:latest
LABEL name="digit-recognizer-pipeline-v1"
LABEL version="latest"

# updating ubuntu packages
RUN apt-get update && yes|apt-get upgrade

# installing necessary libs and adding sudo
RUN apt-get install -y wget sudo

# adding user ubuntu with no password, add to sudo group and setting working directory
RUN adduser --disabled-password --gecos '' ubuntu
RUN adduser ubuntu sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ubuntu
WORKDIR /home/ubuntu/
RUN chmod a+rwx /home/ubuntu/

# getting miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b
RUN rm Miniconda3-latest-Linux-x86_64.sh

# setting conda path
ENV PATH /home/ubuntu/miniconda3/bin:$PATH

# updating conda
RUN conda update conda

# setting project and environment: digit recognizer
RUN mkdir /home/ubuntu/digit_recognizer
COPY . /home/ubuntu/digit_recognizer
RUN conda env create -f /home/ubuntu/digit_recognizer/conda.yml

# setting listening port
EXPOSE 8008

# running application
WORKDIR /home/ubuntu/digit_recognizer/
ENV PYTHONPATH .
CMD ["/home/ubuntu/miniconda3/envs/venv/bin/python", "flask_app/flask_app.py"]