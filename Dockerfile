FROM python:3.6-buster

# Installer ffmpeg avec apt
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]