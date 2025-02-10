from dash import dcc, html
import dash_daq as daq
import plotly.express as px
from db_connection import get_graph1_data, get_graph2_data, get_graph3_data, get_graph4_data

def layout():
    # 1️⃣ Graphique sur la température
    df_temp = get_graph1_data()
    fig_temp = px.line(
        df_temp, x='timestamp', y='temperature',
        title="Évolution de la Température"
    )

    # 2️⃣ Graphique sur le niveau sonore (Jauge)
    df_sound = get_graph2_data()
    # Prenons la valeur la plus récente du niveau sonore
    latest_sound_level = df_sound['sound_level'].iloc[-1] if not df_sound.empty else 0

    # Jauge pour le niveau sonore
    gauge_sound = daq.Gauge(
        id='sound-gauge',
        label="Niveau Sonore",
        value=latest_sound_level,
        min=0,
        max=100,  # Met une valeur max adaptée à ton échelle de son
        showCurrentValue=True,
        units="dB",  # Unité, à adapter en fonction de ce que tu mesures
        color={"gradient": True, "ranges": {"red": [80, 100], "yellow": [40, 80], "green": [0, 40]}},
    )

    # 3️⃣ Graphique sur la qualité de l'air (CO₂)
    df_air = get_graph3_data()
    fig_air = px.line(
        df_air, x='timestamp', y='co2',
        title="Évolution du CO₂ dans la Pièce"
    )

    # 4️⃣ Histogramme sur l'humidité
    df_humidity = get_graph4_data()
    fig_humidity = px.histogram(
        df_humidity, x='humidity', nbins=20,
        title="Distribution de l'Humidité"
    )

    # Mise en page avec 4 graphiques
    return html.Div([
        html.H2("Graphiques des Capteurs", style={'textAlign': 'center'}),
        html.Div([
            html.Div(dcc.Graph(figure=fig_temp), className="graph-container"),
            html.Div(gauge_sound, className="graph-container")  # Remplacement du graphique son par la jauge
        ], className="graph-row"),
        html.Div([
            html.Div(dcc.Graph(figure=fig_air), className="graph-container"),
            html.Div(dcc.Graph(figure=fig_humidity), className="graph-container")
        ], className="graph-row")
    ])
