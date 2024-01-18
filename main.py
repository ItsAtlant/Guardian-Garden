import cv2
import face_recognition
import keyboard
import numpy as np
from cvzone.PoseModule import PoseDetector
from datetime import datetime
from utils import send_email, faces_filter_on, save_photos

# Inizializzazione della videocamera
video_capture = cv2.VideoCapture(0)

# Inizializzazione del rilevatore di posizione
detector = PoseDetector()

# Caricamento dell'immagine di esempio e apprendimento del riconoscimento del volto
davide_image = face_recognition.load_image_file("faces/Davide Soltys.jpg")
davide_face_encoding = face_recognition.face_encodings(davide_image)[0]

trump_image = face_recognition.load_image_file("faces/Donald_Trump_official_portrait.jpg")
trump_face_encoding = face_recognition.face_encodings(trump_image)[0]

# Creazione di una lista di codifiche facciali conosciute e i relativi nomi
known_face_encodings = [
    davide_face_encoding,
    trump_face_encoding
]
known_face_names = [
    "Davide Soltys",
    "Donald Trump"
]

# Inizializzazione di alcune variabili
counter, counter_no_face = 0, 0
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
face_filter = True
number_photos = 0

while True:
    # Cattura di un singolo frame video
    _, frame = video_capture.read()

    # Processa solo ogni altro frame video per risparmiare tempo
    if process_this_frame:
        # Trova i corpi nella scena
        img = detector.findPose(frame, draw=False)
        lmlist, box = detector.findPosition(img)

        # Trova tutti i volti e le relative codifiche nel frame corrente
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []

        # Se non ci sono codifiche facciali ma ci sono corpi rilevati
        if not face_encodings and len(box) > 0:
            counter_no_face += 1
            sensibilita_senza_faccia = 60
            print("Il volto non è rilevato, ma il corpo sì.")
            print("Timer:", sensibilita_senza_faccia - counter_no_face)

            if counter_no_face == sensibilita_senza_faccia:
                current_datetime = str(datetime.now()).replace(":", ".")
            if counter_no_face > sensibilita_senza_faccia:
                if number_photos != 4:
                    output_path, number_photos = save_photos(frame=frame, current_datetime=current_datetime,
                                                              number_photos=number_photos)
                else:
                    send_email(output_path)
                    counter, counter_no_face = 0, 0

        # Per ogni codifica facciale rilevata
        for face_encoding in face_encodings:
            # La funzione "match" restituisce una lista con il valore "true" all'indice della faccia riconosciuta e
            # "false" negli altri indici.
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "SCONOSCIUTO"

            # Ottieni una lista con l'assomiglianza con tutte le facce conosciute
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            # Prendi l'indice con il miglior match nella lista delle facce conosciute
            best_match_index = np.argmin(face_distances)
            # Controlla se il miglior match è vero
            if matches[best_match_index]:
                counter, counter_no_face = 0, 0
                name = known_face_names[best_match_index]
            face_names.append(name)
            sensibilita_faccia_sconosciuta = 20
            if counter == sensibilita_faccia_sconosciuta:
                current_datetime = str(datetime.now()).replace(":", ".")
            if counter > sensibilita_faccia_sconosciuta:
                print("Sospetto nel giardino da solo")
                if number_photos != 4:
                    output_path, number_photos = save_photos(frame=frame, current_datetime=current_datetime,
                                                              number_photos=number_photos)
                else:
                    send_email(output_path)
                    counter, counter_no_face = 0, 0
            print(name, "rilevato")
            counter += 1

    # Visualizza i risultati
    if face_filter:
        faces_filter_on(frame=frame, face_locations=face_locations, face_names=face_names)
    if keyboard.is_pressed('f'):
        face_filter = not face_filter
        cv2.waitKey(1)

    # Premi 'q' sulla tastiera per uscire
    if cv2.waitKey(1) & 0xFF == ord('q') or keyboard.is_pressed('q'):
        break

    # Processa un frame sì e uno no
    process_this_frame = not process_this_frame

    # Visualizza l'immagine risultante
    cv2.imshow('Video', frame)

# Rilascia il controllo della videocamera
video_capture.release()
cv2.destroyAllWindows()

