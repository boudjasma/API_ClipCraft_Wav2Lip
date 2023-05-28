from flask import Flask, request, jsonify
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import datetime

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    title = request.form.get('title').replace(" ","-")
    text = request.form.get('text')
    avatar = "images/avatar"+str(request.form.get('photo'))+".png"
    print(title,text,avatar)

    tts = gTTS(text, lang='fr')
    tts.save("output.wav")

    # Chemin d'accès aux fichiers nécessaires
    checkpoint_path = "checkpoints/wav2lip.pth"
    input_face = avatar
    input_audio = "output.wav"
    output_video = "output_video.mp4"

    # Exécutez Wav2Lip
    os.system(f"python3 inference.py --checkpoint_path {checkpoint_path} --face {input_face} --audio {input_audio} --outfile {output_video}")
    # python3 inference.py --checkpoint_path "checkpoints/wav2lip_gan.pth" --face "images/avatar1.png" --audio "output.wav"
    
    video_path = "temp/result.avi"
    video = VideoFileClip(video_path)
    video_with_audio = video.set_audio(AudioFileClip("output.wav"))

    # Définir le nom et le chemin de la vidéo de sortie
    output_path = f"videos/{title}-{datetime.datetime.now()}.mp4"

    # Sauvegarder la vidéo avec le nouveau fichier audio
    video_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Retournez l'URL de la vidéo générée
    return jsonify({'video_url': output_path})

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello'

if __name__ == '__main__':
    app.run()

