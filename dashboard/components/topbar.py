from dash import html
from db_connection import get_data_topbar
import pandas as pd


def topbar():

    df = get_data_topbar()

    # Vérification des données et formatage
    temperature = df['temperature'].iloc[0] if not df.empty and pd.notna(df['temperature'].iloc[0]) else None
    humidity = df['humidity'].iloc[0] if not df.empty and pd.notna(df['humidity'].iloc[0]) else None
    co2 = df['co2'].iloc[0] if not df.empty and pd.notna(df['co2'].iloc[0]) else None

    # Fonction pour définir la couleur de la température
    def temperature_color(temp):
        if temp is None:
            return 'white', "N/A"  
        elif temp > 30:
            return 'red', f"{temp:.1f}°C"  
        elif temp < 15:
            return 'blue', f"{temp:.1f}°C"  
        else:
            return 'white', f"{temp:.1f}°C"  

    # Fonction pour définir la couleur de l'humidité
    def humidity_color(hum):
        if hum is None:
            return 'white', "N/A"  
        elif hum > 80 or hum < 30:
            return 'red', f"{hum:.1f}%"  
        else:
            return 'white', f"{hum:.1f}%" 

    # Fonction pour définir la couleur du CO2
    def co2_color(c):
        if c is None:
            return 'white', "N/A"  
        elif c > 1000:
            return 'red', f"{c} ppm"  
        else:
            return 'white', f"{c} ppm"  

    # Définir les couleurs et les valeurs formatées
    temp_color, temperature = temperature_color(temperature)
    hum_color, humidity = humidity_color(humidity)
    co2_color, co2 = co2_color(co2)
    
    # Données statiques pour la lumière
    light_level = "750 lux"

    # Organiser les données dans un dictionnaire avec les couleurs
    sensor_data = {
        "Température": (temperature, temp_color),
        "Humidité": (humidity, hum_color),
        "CO2": (co2, co2_color),
        "Etat de la Lumière": (light_level, 'white')  # remplacer par etat 
    }

    cards = [
        html.Div([
            html.H4(title, className="card-title"),
            html.P(value, className="card-value", style={'color': color})
        ], className="sensor-card")
        for title, (value, color) in sensor_data.items()
    ]

    return html.Div(cards, className="topbar")
