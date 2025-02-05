from dash import html
import pandas as pd

# Fausses données simulées
df = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie", "David"],
    "Âge": [25, 30, 35, 40],
    "Ville": ["Paris", "Lyon", "Marseille", "Toulouse"]
})

def layout():
    table_rows = []
    for _, row in df.iterrows():
        table_rows.append(html.Tr([html.Td(row[col]) for col in df.columns], className="table-row"))

    return html.Div([
        html.H2("Tableau de Données", className="page-title"),

        # Tableau des personnes
        html.H3("Informations des utilisateurs", className="section-title"),
        html.Div(
            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in df.columns], className="table-header")),
                html.Tbody(table_rows)
            ], className="styled-table")
        )
    ], className="page-content")
