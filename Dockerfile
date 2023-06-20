FROM python:3.6-buster

# Installer ffmpeg avec apt
RUN apt-get update && apt-get install -y ffmpeg

RUN python3 -m venv /opt/clipcraftapi/venv

RUN pip3 install --upgrade pip  

RUN apt-get clean &&  apt-get autoclean && apt-get autoremove


# copy project
WORKDIR /
ADD . /app
WORKDIR /app

RUN chmod +r checkpoints/wav2lip.pth
RUN chmod +r images/*
RUN chmod -R 777 temp/

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "python3","-u", "app.py" ]