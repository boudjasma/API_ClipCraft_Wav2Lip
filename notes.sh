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
    docker build -t api-wav2lip:v1 .
    docker tag api-wav2lip:v1 us-central1-docker.pkg.dev/driven-lore-383409/my-amazing-container/api-wav2lip:v1 
    gcloud auth configure-docker us-central1-docker.pkg.dev
    docker push us-central1-docker.pkg.dev/driven-lore-383409/my-amazing-container/api-prime:v1

Création de l'image docker :
    docker build -t api-clipcraft-wav2lip:v1.0 .
Run de l'image :
    docker run -p 5000:5000 -it api-clipcraft-wav2lip:v1


Stockage sur google storage :
- Le bucket a été créé manuellement sur gcp

- Sur la ligne de commande : 
    gsutil defacl set public-read gs://clipcraft-bucket1

- Installation des packages necessaires : 
    google-cloud-datastore
    google-cloud-storage
    gunicorn
    google-cloud-core


Text à introduire :
Bonjour, je suis Cloé. En tant que pédiatre, je crois fermement à l'importance d'une approche bienveillante et empathique pour chaque enfant et chaque famille.  
Merci de me rejoindre aujourd'hui et n'hésitez pas à me poser des questions ou à partager vos préoccupations. Je suis là pour vous aider et soutenir la santé de vos enfants.



Deploiement de l'application (django):
docker build -t clipcraftapp:v1.1 .
docker tag clipcraftapp:v1.1 europe-west1-docker.pkg.dev/driven-lore-383409/my-amazing-container/clipcraftapp:v1.1 
gcloud auth configure-docker us-central1-docker.pkg.dev
docker push us-central1-docker.pkg.dev/driven-lore-383409/my-amazing-container/api-prime:v1



Deployer l'app :
gcloud auth login
gcloud auth configure-docker europe-west1-docker.pkg.dev
gcloud config set project clipcraft 
docker tag clipcraftapp:v2.2 europe-west1-docker.pkg.dev/clipcraft/depot-clipcraft-app/clipcraftapp:v2.2
docker push europe-west1-docker.pkg.dev/clipcraft/depot-clipcraft-app/clipcraftapp:v2.2

Deployer l'api :
gcloud auth login
gcloud auth configure-docker europe-west1-docker.pkg.dev
gcloud config set project clipcraft
docker tag clipcraftap:v4 europe-west1-docker.pkg.dev/clipcraft/depot-clipcraft-api/clipcraftap:v4 
docker push europe-west1-docker.pkg.dev/clipcraft/depot-clipcraft-api/clipcraftap:v4

Pour supprimer tous les contenaires qui ne servent à rien :
docker system prune


docker run 864ed9e14f3f sh -c "python manage.py makemigrations && python manage.py migrate"
docker run -i -t 864ed9e14f3f sh
python manage.py createsuperuser
Email address: clipcraftapp@gmail.com 
Password:Clipcraft2023*
Password (again):Clipcraft2023*
Superuser created successfully.


Last trying :
gcloud components install kubectl