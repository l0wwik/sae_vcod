from dash import html

def topbar():
    # Exemple de données des capteurs
    sensor_data = {
        "Température": "22°C",
        "Humidité": "45%",
        "CO2": "380 ppm",
        "Luminosité": "750 lux"
    }

    # Création des cartes pour chaque capteur
    cards = [
        html.Div([
            html.H4(title, className="card-title"),
            html.P(value, className="card-value")
        ], className="sensor-card")
        for title, value in sensor_data.items()
    ]

    # La topbar avec les 4 cartes
    return html.Div(cards, className="topbar")
