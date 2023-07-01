L'api utilise le modèle Wav2Lip qui a été récupéré depuis le dépot https://github.com/Rudrabha/Wav2Lip
Il a été utilisé dans le but d'animer un avatar via un text que l'utilisateur introduit.

Télécharger wav2lip.pth depuis [https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels%2Fwav2lip%2Epth&parent=%2Fpersonal%2Fradrabha%5Fm%5Fresearch%5Fiiit%5Fac%5Fin%2FDocuments%2FWav2Lip%5FModels&ga=1](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?e=TBFBVW) et le mettre dans checkpoits.

Voici les commandes à exécuter afin d'assurer le bon fonctionnement : \n
    sudo apt-get install software-properties-common \n
    sudo add-apt-repository ppa:deadsnakes/ppa \n
    sudo apt update \n
    sudo apt install python3.6 \n
    sudo apt install python3.6-venv \n
    python -m venv vapi \n
    source vapi/bin/activate \n
    sudo apt-get install ffmpeg \n
    pip install --upgrade pip
    pip install -r requirements.txt

Pour run l'API il suffit d'exécuter la commande : 
    python api.py
