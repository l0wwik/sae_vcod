from dash import html, dcc, Input, Output, callback
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
    
    # Obtenir les différentes valeurs possibles pour le filtre des capteurs
    capteur_options = [{"label": capteur, "value": capteur} for capteur in df["capteur"].unique()]

    # Mise en page principale avec le filtre et le tableau
    return html.Div([
        html.H2("Tableau de Données des Capteurs", className="page-title"),
        
        # Dropdown pour filtrer par capteur
        html.Div([
            html.Label("Filtrer par capteur:", className="filter-label"),
            dcc.Dropdown(
                id="capteur-filter",
                options=capteur_options,
                multi=True,
                placeholder="Sélectionnez un ou plusieurs capteurs",
                className="dropdown-filter"
            )
        ], className="filter-container"),
        
        # Tableau des données
        html.Div(id="filtered-table-container", className="table-container")
    ], className="page-content")

# Callback pour mettre à jour le tableau en fonction du filtre
@callback(
    Output("filtered-table-container", "children"),
    Input("capteur-filter", "value")
)
def update_table(selected_capteurs):
    df = get_sensor_data()
    
    if selected_capteurs:
        df = df[df["capteur"].isin(selected_capteurs)]
    
    if df.empty:
        return html.P("Aucune donnée disponible pour les capteurs sélectionnés.", className="no-data-message")

    # Appliquer les unités aux colonnes de données
    df["donnees"] = df.apply(add_units, axis=1)
    
    # Préparer les lignes du tableau
    table_rows = [
        html.Tr([html.Td(row[col]) for col in df.columns], className="table-row")
        for _, row in df.iterrows()
    ]
    
    # Générer le tableau
    return html.Table([
        html.Thead(html.Tr([
            html.Th("Capteur", className="table-header"),
            html.Th("Donnée", className="table-header"),
            html.Th("Date", className="table-header"),
            html.Th("Heure", className="table-header")
        ])),
        html.Tbody(table_rows)
    ], className="styled-table")
