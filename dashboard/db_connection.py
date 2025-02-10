import psycopg2
import pandas as pd

# Fonction pour obtenir une connexion à la base de données
def get_connection():
    return psycopg2.connect(
        dbname="station_captation",
        user="postgres",           
        password="root",  
        host="localhost",
        port="5432"
    )

# Fonction pour exécuter une requête SQL et retourner un DataFrame
def fetch_data(query):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

# données topbar
def get_data_topbar():
    query = """
        SELECT 
            (SELECT temperature FROM sensor_DHT ORDER BY timestamp DESC LIMIT 1) AS temperature,
            (SELECT humidity FROM sensor_DHT ORDER BY timestamp DESC LIMIT 1) AS humidity,
            (SELECT co2 FROM sensor_AirQuality ORDER BY timestamp DESC LIMIT 1) AS co2
    """
    return fetch_data(query)

# Fonction pour récupérer les données de tout les capteurs
def get_sensor_data():
    query = """
        SELECT 'Température' AS capteur, temperature::TEXT AS donnees, timestamp::date AS date, timestamp::time AS heure FROM sensor_DHT
        UNION ALL
        SELECT 'Humidité', humidity::TEXT, timestamp::date, timestamp::time FROM sensor_DHT
        UNION ALL
        SELECT 'CO2', co2::TEXT, timestamp::date, timestamp::time FROM sensor_AirQuality
        UNION ALL
        SELECT 'TVOC', tvoc::TEXT, timestamp::date, timestamp::time FROM sensor_AirQuality
        UNION ALL
        SELECT 'Niveau sonore', sound_level::TEXT, timestamp::date, timestamp::time FROM sensor_Sound
        ORDER BY date DESC, heure DESC
        LIMIT 50;
    """
    return fetch_data(query)

# Fonction pour récupérer les données des 50 dernières entrées
def get_last_entries():
    query = """
        SELECT f.person_name AS nom, i.timestamp::date AS date, i.timestamp::time AS heure, i.image_path
        FROM images i
        LEFT JOIN faces f ON i.id = f.image_id
        ORDER BY i.timestamp DESC
        LIMIT 50;
    """
    return fetch_data(query)

# graph 1
def get_graph1_data():
    query_temp = "SELECT timestamp, temperature FROM sensor_DHT ORDER BY timestamp ASC"
    return fetch_data(query_temp)

# graph 2
def get_graph2_data():
    query_sound = "SELECT timestamp, sound_level FROM sensor_Sound ORDER BY timestamp ASC"
    return fetch_data(query_sound)

# graph 3
def get_graph3_data():
    query_air = """
        SELECT timestamp, co2, tvoc 
        FROM sensor_AirQuality 
        ORDER BY timestamp ASC
    """
    return fetch_data(query_air)

# graph 4
def get_graph4_data():
    query_humidity = "SELECT humidity FROM sensor_DHT"
    return fetch_data(query_humidity)

import pandas as pd
from db_connection import fetch_data

# Etat
def get_state():
    query = """
        SELECT 
            (SELECT sound_level FROM sensor_Sound ORDER BY timestamp DESC LIMIT 1) AS sound,
            (SELECT humidity FROM sensor_DHT ORDER BY timestamp DESC LIMIT 1) AS humidity,
            (SELECT temperature FROM sensor_DHT ORDER BY timestamp DESC LIMIT 1) AS temperature,
            (SELECT tvoc FROM sensor_AirQuality ORDER BY timestamp DESC LIMIT 1) AS tvoc,
            (SELECT co2 FROM sensor_AirQuality ORDER BY timestamp DESC LIMIT 1) AS co2
    """

    df = fetch_data(query)

    if df.empty:
        return 0  

    sound = df["sound"].iloc[0] if pd.notna(df["sound"].iloc[0]) else 0
    humidity = df["humidity"].iloc[0] if pd.notna(df["humidity"].iloc[0]) else 50  
    temperature = df["temperature"].iloc[0] if pd.notna(df["temperature"].iloc[0]) else 22
    tvoc = df["tvoc"].iloc[0] if pd.notna(df["tvoc"].iloc[0]) else 0
    co2 = df["co2"].iloc[0] if pd.notna(df["co2"].iloc[0]) else 400 

    # Vérifications des seuils
    bool_sound = 1 if sound >= 70 else 0
    bool_humidity = 1 if humidity >= 60 or humidity <= 40 else 0
    bool_temp = 1 if temperature >= 25 or temperature <= 18 else 0
    bool_tvoc = 1 if tvoc >= 750 else 0
    bool_co2 = 1 if co2 >= 1000 else 0

    return bool_sound + bool_humidity + bool_temp + bool_tvoc + bool_co2
