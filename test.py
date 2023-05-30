import cv2

# Chemin de la vidéo de l'avatar
video_path = 'temp/result.avi'

# Création de l'objet de capture vidéo
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Conversion de l'image en niveau de gris pour la détection des yeux
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des yeux avec le classificateur de cascade
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Superposition des images des yeux ouverts et fermés sur l'image de la vidéo
    for (x, y, w, h) in eyes:
        # Calcul de la hauteur des paupières pour simuler l'ouverture et la fermeture des yeux
        eyelid_h = int(h / 3)

        # Dessin des paupières supérieure et inférieure
        cv2.rectangle(frame, (x, y), (x + w, y + eyelid_h), (0, 0, 0), -1)  # Paupière supérieure (noir)
        cv2.rectangle(frame, (x, y + 2 * eyelid_h), (x + w, y + h), (0, 0, 0), -1)  # Paupière inférieure (noir)

    # Affichage de l'image
    cv2.imshow('Animated Eyes', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()