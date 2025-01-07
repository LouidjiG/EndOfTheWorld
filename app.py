import dash
from dash import dcc, html

app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap",
    "/assets/style.css" 
])

app.layout = html.Div([
    html.Div(className="headerContainer", children=[
        html.Header([
            html.H1("Logo"),
            html.Ul([
                html.Li(html.A("WHAT", href="#")),
                html.Li(html.A("WHY", href="#")),
                html.Li(html.A("HOW", href="#")),
                html.Li(html.A("SUBSCRIBE", href="#")),
            ])
        ])
    ]),

    html.Section(className="heroSection", children=[
        html.Div(className="backgroundImage first"),
        html.Div(className="backgroundImage second"),

        html.Div(className="counterContainer", children=[
            html.P("Remaining before the end of humanity in", className="remainingTime"),
            dcc.Dropdown(
                id="country",
                options=[
                    {"label": "France", "value": "France"},
                    {"label": "Madagascar", "value": "Madagascar"},
                    {"label": "Togo", "value": "Togo"},
                    {"label": "Algérie", "value": "Algérie"},
                    {"label": "Burkina Faso", "value": "Burkina Faso"},
                    {"label": "Italie", "value": "Italie"},
                    {"label": "Corée", "value": "Corée"},
                    {"label": "Vietnam", "value": "Vietnam"},
                    {"label": "Tchétchénie", "value": "Tchétchénie"},
                    {"label": "Maurice", "value": "Maurice"},
                    {"label": "Chine", "value": "Chine"},
                    {"label": "Liban", "value": "Liban"},
                    {"label": "Maroc", "value": "Marocain"},
                ],
                value="France"
            ),
            html.Div(className="counter", children=[
                html.P("Années"),
                html.P("Mois"),
                html.P("Jours"),
                html.P("Heures"),
                html.P("Minutes"),
                html.P("Secondes"),
                html.P("15 08 27 19 55 03")
            ])
        ]),
        html.A("See more", href="#")
    ]),

    # Section Map
    html.Section(className="map", children=[
        dcc.Dropdown(
            id="filter",
            options=[
                {"label": "Effects on human health", "value": "health"},
                {"label": "Pollution and climate changes", "value": "pollution"},
                {"label": "Biodiversity and alimentary security", "value": "biodiversity"},
                {"label": "Plastic pollution", "value": "plastic"},
            ],
            value="health"
        )
    ]),

    # Section Important Facts

    html.Div(className="fact", children=[html.H3("IMPORTANTS FACTS")]),

    html.Section(className="importantFacts", children=[
        html.Div(className="fact", children=[
            html.H3("MORTS PREMATURES"),
            html.P("79 884 002"),
            html.P("People")
            ]),
        html.Div(className="fact", children=[
            html.H3("PLOMB DANS LE CERVEAU"),
            html.P("800"),
            html.P("Millions d'enfants")
            ]),
        html.Div(className="fact", children=[
            html.H3("PLASTIQUE DANS LE CORPS HUMAIN"),
            html.P("121 000"),
            html.P("Particules de microplastique")
            ]),
        html.Div(className="fact", children=[
            html.H3("REDUCTION DE L'ESPERANCE DE VIE"),
            html.P("-6"),
            html.P("ans")
            ]),

    ]),
    
    html.Div(className="fact", children=[html.H3("Effets du changement climatique")]),

    # Section Facts Graphs
    html.Section(className="factsGraphs", children=[
        html.Div(className="graph"),
        html.Div(className="graph"),
        html.Div(className="graph"),
        html.Div(className="graph"),
    ]),

    # Section Why
    html.Section(className="why", children=[
        html.P("WHY ?"),
        html.P("Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolorum, quis cupiditate quasi sequi doloribus accusamus quae optio facilis esse nulla minus a ipsum perspiciatis dignissimos voluptatibus. Praesentium deserunt sit aperiam."),
    ]),

    # Section Why Graphs
    html.Section(className="whyGraphs", children=[
        html.Div(className="graph"),
        html.Div(className="graph"),
        html.Div(className="graph"),
    ]),

    # Section Main Actors
    html.Section(className="mainActors", children=[
        html.Div(className="country", style={"background": "linear-gradient(to right, #c41313 32.9%, #2E2E2E 100%)"}, children=[
        html.P("32.9%"),
        html.P("CHINA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #c43c13 12.6%, #2E2E2E 100%)"}, children=[
        html.P("12.6%"),
        html.P("USA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, rgb(207, 129, 40) 7%, #2E2E2E 70%)"}, children=[
        html.P("7%"),
        html.P("INDIA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #c4a413 5.1%, #2E2E2E 50%)"}, children=[
        html.P("5.1%"),
        html.P("RUSSIA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #b2c413 2.9%, #2E2E2E 40%)"}, children=[
        html.P("2.9%"),
        html.P("JAPAN", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #80c413 1.9%, #2E2E2E 30%)"}, children=[
        html.P("1.9%"),
        html.P("IRAN", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #28c413 1.8%, #2E2E2E 25%)"}, children=[
        html.P("1.8%"),
        html.P("DEUTSCHLAND", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #31c413 1.7%, #2E2E2E 25%)"}, children=[
        html.P("1.7%"),
        html.P("SOUTH KOREA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #19c413 1.6%, #2E2E2E 20%)"}, children=[
        html.P("1.6%"),
        html.P("INDONESIA", className="countryName")
    ]),
    html.Div(className="country", style={"background": "linear-gradient(to right, #13c413 1.5%, #2E2E2E 20%)"}, children=[
        html.P("1.5%"),
        html.P("SAUDI ARABIA", className="countryName")
    ])
    ]),

    # Section How to Stop
    html.Section(className="howToStop", children=[
        html.Div(className="action"),
        html.Div(className="action"),
        html.Div(className="action"),
        html.Div(className="action"),
    ]),

    # Section Idea
    html.Section(className="idea", children=[
        html.H3("Give us your idea to avoid humanity extinction"),
        html.Form(children=[
            dcc.Input(type="text", placeholder="Email"),
            html.Textarea(placeholder="Give us your idea", id="idea")
        ])
    ]),

    # Footer
    html.Footer(children=[
        html.P("©... Copyrights 2025")
    ])
])

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
