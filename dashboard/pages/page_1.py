from dash import dcc, html
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from db_connection import get_graph1_data, get_graph2_data, get_graph3_data, get_graph4_data

def layout():
    # 1️⃣ Graphique sur la température
    df_temp = get_graph1_data()
    fig_temp = px.line(
        df_temp, x='timestamp', y='temperature',
        title="Évolution de la Température"
    )

    fig_temp.add_hline(y=19, line_dash="dot", line_color="red", annotation_text="Seuil pièce saine (19°C)")

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
    max=100,
    showCurrentValue=True,
    units="dB",
    color={"gradient": True, "ranges": {"red": [80, 100], "yellow": [40, 80], "green": [0, 40]}},
    className="sound-gauge"  # Ajouter une classe personnalisée ici
    )


    # 3️⃣ Graphique sur la qualité de l'air (CO₂)
    df_air = get_graph3_data()
    fig_air = go.Figure()

    # Ajouter la courbe CO₂
    fig_air.add_trace(go.Scatter(
        x=df_air['timestamp'], y=df_air['co2'],
        mode='lines', name="CO₂ (ppm)", line=dict(color='blue')
    ))

    # Ajouter la courbe TVOC
    if 'tvoc' in df_air.columns:
        fig_air.add_trace(go.Scatter(
            x=df_air['timestamp'], y=df_air['tvoc'],
            mode='lines', name="TVOC (ppb)", line=dict(color='green')
        ))

    fig_air.update_layout(title="Évolution du CO₂ et TVOC dans la Pièce")

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
