import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import cv2
import json
import face_recognition

def load_saved_faces(path):
    known_face_names = []
    known_face_encodings = []
    try:

        for face in os.listdir(path):
            known_face_names.append(face.split(".")[0])
            image_loaded = face_recognition.load_image_file(f"{path}/{face}")
            face_encoded = face_recognition.face_encodings(image_loaded)[0]
            known_face_encodings.append(face_encoded)
    except FileNotFoundError:
        print("Errore, file non trovato")

    return known_face_names, known_face_encodings
def get_email_credentials():
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        return config_data.get("email_credentials", {})

def send_email(nome_cartella):
    # Imposta le credenziali del tuo indirizzo email
    credentials = get_email_credentials()
    email_mittente = credentials.get("sender_email")
    password_mittente = credentials.get("sender_password")
    # Imposta l'indirizzo email del destinatario
    email_destinatario = credentials.get("receiver_email")
    # Crea l'oggetto MIME
    messaggio = MIMEMultipart()
    messaggio["From"] = email_mittente
    messaggio["To"] = email_destinatario
    messaggio["Subject"] = "Avviso sicurezza casa"

    # Aggiungi il corpo dell'email
    corpo = "Salve, abbiamo individuato un individuo sospetto nel giardino; ti preghiamo di contattare immediatamente il numero 112 se non riconosci l'estraneo presente."
    messaggio.attach(MIMEText(corpo, "plain"))
    # Legge le foto nella cartella e le aggiunge come allegato
    for nome_immagine in os.listdir(nome_cartella):
        with open(nome_cartella + r"\\" + nome_immagine, "rb") as file_immagine:
            dati_immagine = file_immagine.read()
            immagine_mime = MIMEImage(dati_immagine, name=nome_immagine)
            messaggio.attach(immagine_mime)
    # Stabilisci una connessione con il server SMTP (per Gmail, usa smtp.gmail.com sulla porta 587)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Aggiorna la connessione a una connessione TLS sicura
        server.login(email_mittente, password_mittente)

        # Invia l'email
        server.sendmail(email_mittente, email_destinatario, messaggio.as_string())

    print("Email inviata con successo.")

def faces_filter_on(frame, face_locations, face_names):
    for (alto, destro, basso, sinistro), nome in zip(face_locations, face_names):
        # Disegna un rettangolo intorno al viso
        cv2.rectangle(frame, (sinistro, alto), (destro, basso), (0, 0, 255), 2)

        # Disegna una etichetta con il nome sotto il viso
        cv2.rectangle(frame, (sinistro, basso - 35), (destro, basso), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, nome, (sinistro + 6, basso - 6), font, 1.0, (255, 255, 255), 1)

def save_photos(frame, current_datetime, number_photos):
    percorso_output = f'foto_sospettato{current_datetime}'
    os.makedirs(r"foto_sospettato" + current_datetime, exist_ok=True)
    nome_file_frame = f'{number_photos}fotosospetto.jpg'
    cv2.imwrite(percorso_output + r"//" + nome_file_frame, frame)
    number_photos += 1
    return percorso_output, number_photos
