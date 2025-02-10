from dash import html, dcc
import pandas as pd
from db_connection import get_last_entries


def layout():
    # Récupérer les 50 dernières entrées
    df = get_last_entries()

    # Préparer les lignes du tableau
    table_rows = [
        html.Tr([
            html.Td(row['nom'], className="table-cell"),
            html.Td(row['date'], className="table-cell"),
            html.Td(row['heure'], className="table-cell"),
            html.Td(html.Img(src=f"/assets/img/{row['image_path']}", className="camera-image"), className="table-cell")
        ], className="table-row")
        for _, row in df.iterrows()
    ]

    return html.Div([
        html.H2("Entrées dans la pièce", className="page-title"),

        # Dernière capture de la caméra (si besoin)
        html.H3("Dernière capture de la caméra", className="section-title"),
        html.Div(html.Img(src=f"/assets/img/{df.iloc[0]['image_path']}", className="camera-image") if not df.empty else "Aucune capture disponible"),

        # Tableau des entrées
        html.H3("Tableau des entrées", className="section-title"),
        html.Div(
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Nom", className="table-header"),
                    html.Th("Date", className="table-header"),
                    html.Th("Heure", className="table-header"),
                    html.Th("Image", className="table-header")
                ])),
                html.Tbody(table_rows)
            ], className="styled-table")
        )
    ], className="page-content")
