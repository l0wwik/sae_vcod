from dash import html, dcc
import pandas as pd

# Fausses données simulées
data = {
    "Nom": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Heure d'entrée": ["10:00", "10:05", "10:15", "10:20", "10:30"],
    "ID Badge": [101, 102, 103, 104, 105]
}
df = pd.DataFrame(data)

def layout():
    table_rows = []
    for _, row in df.iterrows():
        table_rows.append(html.Tr([html.Td(row[col]) for col in df.columns], className="table-row"))

    return html.Div([
        html.H2("Entrées dans la pièce", className="page-title"),
        
        # Image de la caméra
        html.H3("Dernière capture de la caméra", className="section-title"),
        html.Div(html.Img(src="/assets/img/placeholder.png", className="camera-image")),

        # Tableau des personnes
        html.H3("Tableau des entrées", className="section-title"),
        html.Div(
            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in df.columns], className="table-header")),
                html.Tbody(table_rows)
            ], className="styled-table")
        )
    ], className="page-content")
