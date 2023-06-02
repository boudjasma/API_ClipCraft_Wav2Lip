from flask import Flask, request, jsonify
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import datetime
from google.cloud import storage
import cv2
import numpy as np

_BUCKET_NAME = 'clipcraft-bucket1'

app = Flask(__name__)


def text_to_vid(title, text, avatar):
    # Text to speech
    tts = gTTS(text, lang='fr')
    tts.save("speech.wav")

    # Wav2Lip 
    checkpoint_path = "checkpoints/wav2lip.pth"
    input_face = f"images/{avatar}.png"  # Remplacez par le chemin de votre fichier PNG
    input_audio = "speech.wav"

    os.system(f"python inference.py --checkpoint_path {checkpoint_path} --face {input_face} --audio {input_audio}")

    # Video generating with moviepy
    video = VideoFileClip("temp/result.avi")
    video_with_audio = video.set_audio(AudioFileClip(input_audio))
    video_path = f"videos/{title}.mp4"
    video_with_audio.write_videofile(video_path, codec="libx264", audio_codec="aac")

    os.remove("temp/result.avi")
    os.remove("speech.wav")
    
    return video_path

def stockage_on_gs(video_path, title):
    _BUCKET_NAME = 'clipcraft-bucket1'

    # Connexion to google storage
    gcs_client = storage.Client.from_service_account_json("key.json")
    bucket = gcs_client.get_bucket(_BUCKET_NAME)
    blob = bucket.blob(title)

    video = cv2.VideoCapture(video_path)

    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = []

    # Lire les frames de la vidéo et les stocker dans la liste
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)

    frames_array = np.array(frames)
    output_video = cv2.VideoWriter(filename=None, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=fps, frameSize=(frame_width, frame_height))

    for frame in frames_array:
        output_video.write(frame)

    # Stockage on google storage
    output_video.release()
    blob.upload_from_filename(video_path)

    url = blob.public_url
    print("Fichier vidéo stocké avec succès !")
    print("Lien de téléchargement : {}".format(url))

    # Remove from local
    os.remove(video_path)

    return url




@app.route('/generate-video', methods=['POST'])
def generate_video():
    title = request.form.get('title').replace(" ","-").replace(".","-").replace(":","")
    text = request.form.get('text')
    avatar = "avatar"+str(request.form.get('photo'))

    print(title,text,avatar)
    # video = text_to_vid(title,text, avatar)
    # url = stockage_on_gs(video,title)
    url="https://storage.googleapis.com/clipcraft-bucket1/Alexisc-Clo%C3%A9-p%C3%A9diatre-2023-06-03-011502-918333"

    return jsonify({'video_url': format(url)})

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello'

if __name__ == '__main__':
    app.run()

