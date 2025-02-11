import paho.mqtt.client as mqtt
import psycopg2
import json
import numpy as np
import time
import os
from keras_facenet import FaceNet
import cv2
from PIL import Image
import io

# 📡 Configuration MQTT
MQTT_BROKER = "192.168.8.5"
MQTT_PORT = 1883
MQTT_IMAGE_TOPIC = "station04/sensor/image"
IMAGE_DIR = "C:/Users/loicm/Desktop/image_user"

# 💾 Connexion PostgreSQL
DB_NAME = "station_captation"
DB_USER = "postgres"
DB_PASSWORD = "Youtubel0wwik55110**"
DB_HOST = "localhost"

# 🚀 Initialisation du modèle FaceNet (512 dimensions)
embedder = FaceNet()

# 🔄 Buffer pour stocker l’image avant reconstitution
image_chunks = []
receiving_image = False

def connect_db():
    """Connexion à PostgreSQL"""
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

# 📸 Sauvegarde et détection des visages
def process_image(image_data):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"{IMAGE_DIR}/image_{timestamp}.jpg"

    try:
        # 📌 Convertir l'image reçue en format exploitable
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")
        image.save(image_path)

        # 📸 Chargement de l'image avec OpenCV
        image_cv = cv2.imread(image_path)
        if image_cv is None:
            print(f"🚨 Erreur : Impossible de charger l’image {image_path}")
            return None, None

        # 🔥 Détection des visages et extraction des embeddings (512 dimensions)
        faces = embedder.extract(image_cv, threshold=0.95)

        if len(faces) == 0:
            print("🚨 Aucun visage détecté")
            return None, None

        # 🔍 Stocker les visages reconnus ou inconnus
        for face in faces:
            box = face['box']  # Coordonnées du visage (x, y, largeur, hauteur)
            embedding_vector = np.array(face['embedding'], dtype=np.float32)  # 🔹 Stockage en 512 dimensions
            print(f"📏 Taille de l'embedding généré : {len(embedding_vector)}")  # Vérification

            person_name = find_matching_face(embedding_vector)

            if person_name is None:
                person_name = "Unknown"
                save_face_embedding(image_path, person_name, embedding_vector)

            # 🟩 Dessiner un carré autour du visage et ajouter le nom
            x, y, w, h = box
            cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Carré vert
            cv2.putText(image_cv, person_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 🖼️ Sauvegarder l’image annotée
        annotated_path = image_path.replace(".jpg", "_annotated.jpg")
        cv2.imwrite(annotated_path, image_cv)
        print(f"✅ Image annotée sauvegardée : {annotated_path}")

        return annotated_path, embedding_vector

    except Exception as e:
        print(f"❌ Erreur lors du traitement de l'image : {e}")
        return None, None

# 🔍 Vérifier si un visage existe déjà en base
def find_matching_face(new_embedding):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, person_name, embedding FROM faces;")
    results = cursor.fetchall()
    
    best_match = None
    best_distance = float("inf")

    for face_id, name, stored_embedding in results:
        stored_embedding = np.array(stored_embedding, dtype=np.float32)  # 🔹 Conversion correcte
        new_embedding = np.array(new_embedding, dtype=np.float32)  # 🔹 Assurer la même conversion

        if stored_embedding.shape == new_embedding.shape:  # 🔹 Comparer seulement si la taille est identique
            distance = np.linalg.norm(stored_embedding - new_embedding)
            if distance < best_distance:
                best_distance = distance
                best_match = (face_id, name)

    conn.close()

    if best_distance < 0.7:  # Seuil FaceNet
        print(f"✅ Visage reconnu : {best_match[1]} (distance {best_distance:.4f})")
        return best_match[1]
    else:
        print("❌ Aucun visage correspondant trouvé")
        return None

# 💾 Enregistrer un nouvel embedding
def save_face_embedding(image_path, person_name, embedding):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO faces (timestamp, image_id, person_name, embedding, created_at, updated_at)
        VALUES (%s, (SELECT id FROM images WHERE image_path = %s), %s, %s, %s, %s);
    """, (time.strftime("%Y-%m-%d %H:%M:%S"), image_path, person_name, embedding.tolist(), time.strftime("%Y-%m-%d %H:%M:%S"), time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"🧑‍💻 Nouveau visage enregistré : {person_name}")

# 📡 Callback pour réception des messages MQTT
def on_message(client, userdata, msg):
    global image_chunks, receiving_image

    print(f"📥 Message reçu sur {msg.topic}")

    if msg.topic == MQTT_IMAGE_TOPIC:
        payload = msg.payload

        if payload == b"END":
            full_image_data = b"".join(image_chunks)
            image_chunks = []
            receiving_image = False

            annotated_path, embedding_vector = process_image(full_image_data)

            if annotated_path:
                print(f"✅ Image annotée enregistrée : {annotated_path}")

        else:
            try:
                chunk_id, chunk_data = payload.split(b"|", 1)
                image_chunks.append(chunk_data)
                receiving_image = True
            except ValueError:
                print("❌ Erreur : Format du chunk invalide")

# 📡 Connexion MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

# 🔔 S'abonner aux topics des capteurs et images
client.subscribe("station04/sensor/#")
client.on_message = on_message

print("📡 En attente des messages MQTT...")
client.loop_forever()

