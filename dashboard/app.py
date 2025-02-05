import dash
from dash import dcc, html, Input, Output
from navbar import sidebar
from pages import page_1, page_2, page_3  # Import des pages

# Initialisation de l'application
app = dash.Dash(__name__)
app.title = "Dashboard"
server = app.server  # Pour déploiement sur un serveur si nécessaire

# Styles pour le contenu
CONTENT_STYLE = {
    "marginLeft": "270px",
    "padding": "20px"
}

# Mise en page principale
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,  # Barre de navigation latérale
    html.Div(id='page-content', style=CONTENT_STYLE)
])

# Callback pour afficher la bonne page
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-2':
        return page_2.layout()
    elif pathname == '/page-3':
        return page_3.layout()
    else:  # Page 1 par défaut
        return page_1.layout()

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
