from dash import html
import pandas as pd
from db_connection import get_sensor_data


# Fonction pour ajouter les unités aux données
def add_units(row):
    unit_map = {
        "Température": "°C",
        "Humidité": "%",
        "CO2": "ppm",
        "TVOC": "ppb",
        "Niveau sonore": "dB"
    }
    capteur = row["capteur"]
    valeur = row["donnees"]
    return f"{valeur} {unit_map.get(capteur, '')}"

# Fonction pour générer la mise en page
def layout():
    df = get_sensor_data()
    
    if df.empty:
        return html.Div([
            html.H2("Tableau de Données", className="page-title"),
            html.P("Aucune donnée disponible.", className="no-data-message")
        ])

    # Appliquer les unités aux colonnes de données
    df["donnees"] = df.apply(add_units, axis=1)

    # Préparer les lignes du tableau
    table_rows = [
        html.Tr([html.Td(row[col]) for col in df.columns], className="table-row")
        for _, row in df.iterrows()
    ]

    return html.Div([
        html.H2("Tableau de Données des Capteurs", className="page-title"),
        html.Div(
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Capteur", className="table-header"),
                    html.Th("Donnée", className="table-header"),
                    html.Th("Date", className="table-header"),
                    html.Th("Heure", className="table-header")
                ])),
                html.Tbody(table_rows)
            ], className="styled-table")
        )
    ], className="page-content")
