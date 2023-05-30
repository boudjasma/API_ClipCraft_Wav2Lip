FROM python:3.6-buster

# Installer ffmpeg avec apt
RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir /opt/clipcraftapi \
        && python3 -m venv /opt/clipcraftapi/venv

WORKDIR /opt/clipcraftapi

COPY . /opt/clipcraftapi

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "./opt/clipcraftapi/app.py" ]