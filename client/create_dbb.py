import duckdb
import os
import time

DB_PATH = "images.duckdb"
IMAGE_DIR = "received_images"

# Assure-toi que le dossier images existe
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Connexion à la base DuckDB et création de la table
def init_db():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id BIGINT,  -- DuckDB ne supporte pas PRIMARY KEY, on gère manuellement l'ID
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT NOT NULL,
            sensor_trigger TEXT NOT NULL
        )
    """)
    conn.close()

# Fonction pour récupérer le dernier ID et l'incrémenter
def get_next_id():
    conn = duckdb.connect(DB_PATH)
    result = conn.execute("SELECT MAX(id) FROM images").fetchone()[0]
    conn.close()
    return 1 if result is None else result + 1

# Fonction pour sauvegarder une image
def save_image(image_data, sensor_trigger="PIR"):
    """Sauvegarde l'image sur le Raspberry Pi et enregistre son chemin dans DuckDB"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_path = f"{IMAGE_DIR}/image_{timestamp}.jpg"
    image_id = get_next_id()  # Récupère l'ID auto-incrémenté

    # Sauvegarde l'image
    with open(image_path, "wb") as img_file:
        img_file.write(image_data)

    # Insère l'image dans DuckDB
    conn = duckdb.connect(DB_PATH)
    conn.execute("INSERT INTO images (id, image_path, sensor_trigger) VALUES (?, ?, ?)", (image_id, image_path, sensor_trigger))
    conn.close()

    print(f"✅ Image sauvegardée : {image_path} (ID: {image_id})")
    return image_path

# Initialisation de la base
init_db()

# Simule l'enregistrement d'une image (test)
dummy_data = b"\xff\xd8\xff\xdb\x00\x43\x00..."  # Contenu binaire d'une image JPEG
save_image(dummy_data, "Test")
