FROM python:3.6-buster

# Installer ffmpeg avec apt
RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --upgrade pip  

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD flask run -h 0.0.0.0 -p 5000