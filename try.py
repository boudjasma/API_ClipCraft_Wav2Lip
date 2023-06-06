import io
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import storage
import cv2
import numpy as np
import torch



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

    download_url = blob.public_url
    print("Fichier vidéo stocké avec succès !")
    print("Lien de téléchargement : {}".format(download_url))

    # Remove from local
    os.remove(video_path)

    return download_url



# video = text_to_vid('ma-video','Ceci est juste un test', 'avatar8')
# stockage_on_gs(video,'ma-video')



def load_wav2lip_model_from_gcs(bucket_name, model_path):
    storage_client = storage.Client.from_service_account_json("key.json")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(model_path)
    model_bytes = blob.download_as_bytes()
    model = torch.load(io.BytesIO(model_bytes), map_location=torch.device('cpu'))
    return model
