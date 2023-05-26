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


Pour le cloud :
- Télécharger Google Cloud CLI
    vérifier avec la commande suivante : gcloud --version
- Se connecter au compte GCP :
    Exécutez la commande suivante pour ce faire : gcloud auth login
    Ensuite : gcloud components update
- Dans le projet local, lancer la commande suivante : 
    gcloud init
- Exécuter les commandes : 
    docker build -t api-prime:v1 .
    docker tag api-prime:v1 us-central1-docker.pkg.dev/driven-lore-383409/my-amazing-container/api-prime:v1 
    gcloud auth configure-docker us-central1-docker.pkg.dev
    docker push us-central1-docker.pkg.dev/driven-lore-383409/my-amazing-container/api-prime:v1
