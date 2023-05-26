import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

# Générez le fichier audio avec gTTS
text = "Salam est ce que ça va marcher ? J'ai trop peur..."
tts = gTTS(text, lang='fr')
tts.save("output.wav")

# Chemin d'accès aux fichiers nécessaires
checkpoint_path = "checkpoints/wav2lip.pth"
input_face = "images/avatar2.png"  # Remplacez par le chemin de votre fichier PNG
input_audio = "output.wav"
output_video = "output_video.mp4"

# Exécutez Wav2Lip
os.system(f"python3 inference.py --checkpoint_path {checkpoint_path} --face {input_face} --audio {input_audio} --outfile {output_video}")

video_path = "temp/result.avi"
video = VideoFileClip(video_path)
video_with_audio = video.set_audio(AudioFileClip("output.wav"))

# Définir le nom et le chemin de la vidéo de sortie
output_path = "video_generated_1.mp4"

# Sauvegarder la vidéo avec le nouveau fichier audio
video_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")