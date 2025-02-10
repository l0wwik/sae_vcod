from dash import dcc, html
import plotly.express as px
from db_connection import fetch_data  # Import de la fonction fetch_data

def layout():
    # 1️⃣ Graphique sur la température
    query_temp = "SELECT timestamp, temperature FROM sensor_DHT ORDER BY timestamp ASC"
    df_temp = fetch_data(query_temp)
    fig_temp = px.line(
        df_temp, x='timestamp', y='temperature',
        title="Évolution de la Température"
    )

    # 2️⃣ Graphique sur le niveau sonore
    query_sound = "SELECT timestamp, sound_level FROM sensor_Sound ORDER BY timestamp ASC"
    df_sound = fetch_data(query_sound)
    fig_sound = px.line(
        df_sound, x='timestamp', y='sound_level',
        title="Niveau Sonore dans la Pièce"
    )

    # 3️⃣ Graphique sur la qualité de l'air (CO₂)
    query_air = "SELECT timestamp, co2 FROM sensor_AirQuality ORDER BY timestamp ASC"
    df_air = fetch_data(query_air)
    fig_air = px.line(
        df_air, x='timestamp', y='co2',
        title="Évolution du CO₂ dans la Pièce"
    )

    # 4️⃣ Histogramme sur l'humidité
    query_humidity = "SELECT humidity FROM sensor_DHT"
    df_humidity = fetch_data(query_humidity)
    fig_humidity = px.histogram(
        df_humidity, x='humidity', nbins=20,
        title="Distribution de l'Humidité"
    )

    # Mise en page avec 4 graphiques
    return html.Div([
        html.H2("Graphiques des Capteurs", style={'textAlign': 'center'}),
        html.Div([
            html.Div(dcc.Graph(figure=fig_temp), className="graph-container"),
            html.Div(dcc.Graph(figure=fig_sound), className="graph-container")
        ], className="graph-row"),
        html.Div([
            html.Div(dcc.Graph(figure=fig_air), className="graph-container"),
            html.Div(dcc.Graph(figure=fig_humidity), className="graph-container")
        ], className="graph-row")
    ])
