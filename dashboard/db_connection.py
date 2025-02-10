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
