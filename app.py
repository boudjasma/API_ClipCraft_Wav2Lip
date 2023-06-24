from flask import Flask, request, jsonify
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import datetime
from google.cloud import storage
import cv2
import numpy as np
from google.cloud import texttospeech
from google.oauth2 import service_account

_BUCKET_NAME = 'clipcraft-bucket1'
def auth_GCP(path_key): 
    credentials_path = path_key
    service_account.Credentials.from_service_account_file(credentials_path)

def Text2wave(text, output_file, gender, path_key):
    auth_GCP(path_key)
    client = texttospeech.TextToSpeechClient()
    if gender=="male":
        voice= texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name="fr-FR-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        
    else:
        voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name="fr-FR-Wavenet-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    synthesis_input = texttospeech.SynthesisInput(text=text)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    with open(output_file, "wb") as out_file:
        out_file.write(response.audio_content)

    print(f'Audio content written to "{output_file}"') #noqa


def text_to_vid(title, text, avatar, gender): 
    Text2wave(text,"speech.wav", gender,"key.json")

    # Wav2Lip 
    checkpoint_path = "checkpoints/wav2lip.pth"
    input_face = f"images/{avatar}.png"
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
    print("Fichier vidéo stocké avec succès !") #noqa
    print("Lien de téléchargement : {}".format(url)) #noqa

    # Remove from local
    os.remove(video_path)

    return url

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    title = request.form.get('title').replace(" ","-").replace(".","-").replace(":","")
    text = request.form.get('text')    
    gender = request.form.get('photo')
    avatar = "avatar"+str(gender)
    print(title,text,avatar) #noqa

    gender="female"if gender in [1,2,5,6,8] else "male"

    video = text_to_vid(title,text, avatar, gender)
    url = stockage_on_gs(video,title)

    print(url)
    return jsonify({'video_url': url})

@app.route('/', methods=['GET'])
def get():
    return jsonify(message='Hello from ClipCraft Api !')


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port='5000')
