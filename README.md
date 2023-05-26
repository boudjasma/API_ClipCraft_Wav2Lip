L'api utilise le modèle Wav2Lip qui a été récupéré depuis le dépot https://github.com/Rudrabha/Wav2Lip
Il a été utilisé dans le but d'animer un avatar via un text que l'utilisateur introduit.
Voici les commandes à exécuter afin d'assurer le bon fonctionnement : 

sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
sudo apt install python3.6-venv
python -m venv vapi
source vapi/bin/activate
sudo apt-get install ffmpeg
pip install --upgrade pip
pip install -r requirements.txt

Pour run l'API il suffit d'exécuter la commande : 
python api.py