from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuration de la connexion PostgreSQL
DATABASE_URL = "dbname=station_captation user=postgres password=Youtubel0wwik55110** host=localhost port=5432"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Endpoint pour obtenir toutes les images
@app.route('/images', methods=['GET'])
def get_images():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM images;')
    images = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(images), 200

# Endpoint pour obtenir les relevés du capteur DHT
@app.route('/sensor_dht', methods=['GET'])
def get_sensor_dht():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM sensor_DHT;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200

# Endpoint pour obtenir les relevés du capteur PIR
@app.route('/sensor_pir', methods=['GET'])
def get_sensor_pir():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM sensor_PIR;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200

# Endpoint pour obtenir les relevés du capteur sonore
@app.route('/sensor_sound', methods=['GET'])
def get_sensor_sound():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM sensor_Sound;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200

# Endpoint pour obtenir les relevés du capteur de qualité de l'air
@app.route('/sensor_air_quality', methods=['GET'])
def get_sensor_air_quality():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM sensor_AirQuality;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200

# Endpoint pour obtenir toutes les empreintes faciales
@app.route('/faces', methods=['GET'])
def get_faces():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM faces;')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data), 200

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
