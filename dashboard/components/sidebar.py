from dash import html, dcc

sidebar = html.Div([
    html.H2("Navigation", className="sidebar-title"),
    html.Nav([
        dcc.Link(
            html.Span([
                html.Img(src="/assets/img/page1_ico.svg", className="icon"),
                "Graphiques"
            ]), href='/page-1', className="sidebar-link"
        ),
        dcc.Link(
            html.Span([
                html.Img(src="/assets/img/page2_ico.svg", className="icon"),
                "Préscence"
            ]), href='/page-2', className="sidebar-link"
        ),
        dcc.Link(
            html.Span([
                html.Img(src="/assets/img/page3_ico.svg", className="icon"),
                "Tableau"
            ]), href='/page-3', className="sidebar-link"
        )
    ])
], className="sidebar")
