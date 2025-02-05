from dash import dcc, html
import plotly.express as px

# Chargement des données
df = px.data.gapminder()

def layout():
    # 1. Graphique en courbes (Line chart)
    fig_line = px.line(
        df[df['country'] == 'France'], x='year', y='gdpPercap',
        title="Évolution du PIB par habitant en France"
    )

    # 2. Diagramme circulaire (Pie chart)
    fig_pie = px.pie(
        df[df['year'] == 2007], names='continent', values='pop',
        title="Répartition de la population mondiale par continent (2007)"
    )

    # 3. Graphique en barres (Bar chart)
    fig_bar = px.bar(
        df[df['year'] == 2007].nlargest(10, 'pop'),
        x='country', y='pop', color='continent',
        title="10 pays les plus peuplés en 2007"
    )

    # 4. Histogramme
    fig_hist = px.histogram(
        df[df['year'] == 2007], x='lifeExp', nbins=20,
        title="Distribution de l'espérance de vie (2007)"
    )

    # Mise en page avec 4 graphiques
    return html.Div([
        html.H2("Graphiques Interactifs", style={'textAlign': 'center'}),
        html.Div([
            html.Div(dcc.Graph(figure=fig_line), className="graph-container"),
            html.Div(dcc.Graph(figure=fig_pie), className="graph-container")
        ], className="graph-row"),
        html.Div([
            html.Div(dcc.Graph(figure=fig_bar), className="graph-container"),
            html.Div(dcc.Graph(figure=fig_hist), className="graph-container")
        ], className="graph-row")
    ])
