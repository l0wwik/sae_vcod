import paho.mqtt.client as mqtt
import psycopg2
import json
import numpy as np
import time
import os
from keras_facenet import FaceNet
import cv2

# 📡 Paramètres de connexion MQTT
MQTT_BROKER = "192.168.8.5"
MQTT_PORT = 1883
MQTT_TOPICS = [
    "station04/sensor/DHT",
    "station04/sensor/PIR",
    "station04/sensor/Sound",
    "station04/sensor/Airquality",
    "station04/sensor/image"
]

# 💾 Paramètres PostgreSQL
DB_NAME = "station_captation"
DB_USER = "postgres"
DB_PASSWORD = "Youtubel0wwik55110**"
DB_HOST = "localhost"
IMAGE_DIR = "C:/Users/loicm/Desktop/image_user"

# 🚀 Charger le modèle FaceNet pour l'extraction des embeddings
embedder = FaceNet()

# 📡 Connexion à PostgreSQL
def connect_db():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

# 📸 Sauvegarde d'une Image et Extraction de l'Embedding
def process_image(image_data):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    image_path = f"{IMAGE_DIR}/image_{timestamp.replace(':', '-')}.jpg"

    # Sauvegarde de l'image sur le disque
    with open(image_path, "wb") as img_file:
        img_file.write(image_data)

    # Chargement et prétraitement de l'image pour FaceNet
    image = cv2.imread(image_path)
    faces = embedder.extract(image, threshold=0.95)  # Détection de visage + extraction embedding

    if len(faces) == 0:
        print("🚨 Aucun visage détecté dans l'image.")
        return None, None

    embedding_vector = faces[0]['embedding']
    return image_path, embedding_vector

# 🧑‍💻 Vérifier si un visage existe déjà en base
def find_matching_face(new_embedding):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, person_name, embedding FROM faces;")
    results = cursor.fetchall()
    
    best_match = None
    best_distance = float("inf")

    for face_id, name, stored_embedding in results:
        stored_embedding = np.array(stored_embedding)
        distance = np.linalg.norm(stored_embedding - new_embedding)
        if distance < best_distance:
            best_distance = distance
            best_match = (face_id, name)

    conn.close()

    if best_distance < 0.7:  # Seuil FaceNet
        print(f"✅ Visage reconnu : {best_match[1]} (distance {best_distance:.4f})")
        return best_match[1]  # Retourne le nom de la personne
    else:
        print("❌ Aucun visage correspondant trouvé")
        return None

# 🧑‍💻 Enregistrement d'un Nouvel Embedding
def save_face_embedding(image_id, person_name, embedding):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO faces (timestamp, image_id, person_name, embedding, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (time.strftime("%Y-%m-%d %H:%M:%S"), image_id, person_name, embedding.tolist(), time.strftime("%Y-%m-%d %H:%M:%S"), time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"🧑‍💻 Nouveau visage enregistré sous le nom : {person_name}")

# 📡 Enregistrement des données des capteurs
def save_sensor_data(topic, payload):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect_db()
    cursor = conn.cursor()

    try:
        data = json.loads(payload)

        if topic == "station04/sensor/DHT":
            cursor.execute("""
                INSERT INTO sensor_DHT (timestamp, temperature, humidity, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s);
            """, (timestamp, data["temperature"], data["humidity"], timestamp, timestamp))

        elif topic == "station04/sensor/PIR":
            cursor.execute("""
                INSERT INTO sensor_PIR (timestamp, motion_detected, created_at, updated_at)
                VALUES (%s, %s, %s, %s);
            """, (timestamp, data["move"], timestamp, timestamp))

        elif topic == "station04/sensor/Sound":
            cursor.execute("""
                INSERT INTO sensor_Sound (timestamp, sound_level, created_at, updated_at)
                VALUES (%s, %s, %s, %s);
            """, (timestamp, data["Sound"], timestamp, timestamp))

        elif topic == "station04/sensor/Airquality":
            cursor.execute("""
                INSERT INTO sensor_AirQuality (timestamp, co2, tvoc, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s);
            """, (timestamp, data["co2"], data["TVoC"], timestamp, timestamp))

        conn.commit()
        print(f"📡 Données enregistrées pour {topic}")

    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement des capteurs : {e}")

    conn.close()

# 🚀 Callback pour réception des messages MQTT
def on_message(client, userdata, msg):
    print(f"📥 Message reçu sur {msg.topic}")

    if msg.topic == "station04/sensor/image":
        image_path, embedding_vector = process_image(msg.payload)

        if embedding_vector is not None:
            existing_person = find_matching_face(embedding_vector)
            if existing_person is None:
                save_face_embedding(image_path, "Unknown", embedding_vector)  # Enregistre avec le tag "Unknown"

    elif msg.topic.startswith("station04/sensor/"):
        save_sensor_data(msg.topic, msg.payload)

# 📡 Connexion MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

# 🔔 S'abonner aux topics des capteurs et images
for topic in MQTT_TOPICS:
    client.subscribe(topic)

client.on_message = on_message

print("📡 En attente des messages MQTT...")
client.loop_forever()
