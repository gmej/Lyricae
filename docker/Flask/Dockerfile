FROM python:3.7

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo


RUN sudo apt-get update -y
RUN sudo apt-get install -y git nodejs npm 
RUN git clone https://github.com/gmej/Lyricae
#python-pip python-dev build-essential python3-venv python3-pip python3.7
ENV ROOT /Lyricae
ENV APP_PATH /Lyricae/app

# Change directory
WORKDIR $ROOT
#RUN pip install -v requests -i https://pypi.python.org/simple/
#RUN pip install --upgrade setuptools pip wheel
#RUN python3 -m pip install -U -r requirements.txt
RUN python --version
RUN pip install -r requirements.txt 

WORKDIR $APP_PATH

RUN npm install
ENV FLASK_APP api.py
CMD npm run start-api

EXPOSE 5000