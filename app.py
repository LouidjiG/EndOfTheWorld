import dash
from dash import dcc, html
from fetch_data.fetch_natural_disaster_data import get_natural_disaster_data, visualize_natural_disaster_data
from dash.dependencies import Input, Output, State
import datetime
from fetch_data.calculate_doomsday_year import calculate_doomsday_year, calculate_time_left

doomsday_country_cache = {}

app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap",
    "/assets/style.css" 
])


country = {
    "France": "FRA", 
    "Italie": "ITA", 
    "Chine": "CHN", 
    "Madagascar": "MDG", 
    "Thétchénie": "RUS", 
    "Togo": "TGO", 
    "Corée": "KOR",
    "Vietnam": "VNM", 
    "Algérie": "DZA", 
    "Burkina Faso": "BFA", 
    "Maurice": "MUS", 
    "Liban": "LBN", 
    "Maroc": "MAR"
    }

app.layout = html.Div([
    html.Section(className="heroSection", id="heroSection", children=[
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
                    {"label": "Burkina Faso", "value": "BurkinaFaso"},
                    {"label": "Italie", "value": "Italie"},
                    {"label": "Corée", "value": "Corée"},
                    {"label": "Vietnam", "value": "Vietnam"},
                    {"label": "Tchétchénie", "value": "Tchétchénie"},
                    {"label": "Maurice", "value": "Maurice"},
                    {"label": "Chine", "value": "Chine"},
                    {"label": "Liban", "value": "Liban"},
                    {"label": "Maroc", "value": "Maroc"},
                ],
                value="France"
            ),
            html.Div(className="counter", children=[
                
                html.Div(className="countDiv", children=[
                    html.P("ANNEES"),
                    html.P(id="years", children=0),
                ]),
                html.Div(className="countDiv", children=[
                    html.P("MOIS"),
                    html.P(id="months", children=0),
                ]),
                html.Div(className="countDiv", children=[
                    html.P("JOURS"),
                    html.P(id="days", children=0),
                ]),
                html.Div(className="countDiv", children=[
                    html.P("HEURES"),
                    html.P(id="hours", children=0),
                ]),
                html.Div(className="countDiv", children=[
                    html.P("MINUTES"),
                    html.P(id="minutes", children=0),
                ]),
                html.Div(className="countDiv", children=[
                    html.P("SECONDES"),
                    html.P(id="seconds", children=0),
                ])
            ])
        ]),

        dcc.Interval(
            id="interval-component",
            interval=1000,  # 1 seconde (1000 ms)
            n_intervals=0,  # Initialisation
        )
        
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

    


    html.Div(className="fact", children=[html.H3("CLIMATE CHANGING EFFECTS")]),


    

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
        html.H2("C'EST DE LEUR FAUTE"),
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

@app.callback(
    [
        Output("years", "children"),
        Output("months", "children"),
        Output("days", "children"),
        Output("hours", "children"),
        Output("minutes", "children"),
        Output("seconds", "children"),
    ],
    [
        Input("interval-component", "n_intervals"),
        Input("country", "value")
    ]
)
def update_counter(n_intervals, selected_country):
    if selected_country not in doomsday_country_cache:
        doomsday_country_cache[selected_country] = calculate_doomsday_year(country[selected_country])
    doomsday_year = doomsday_country_cache[selected_country]
    
    current_date = datetime.datetime.now()
    years_left = doomsday_year - current_date.year
    months_left = 12 - current_date.month
    days_left = 31 - current_date.day
    hours_left = 24 - current_date.hour
    minutes_left = 60 - current_date.minute
    seconds_left = 60 - current_date.second

    return years_left, months_left, days_left, hours_left, minutes_left, seconds_left
    
@app.callback(
    Output("heroSection", "style"),  # Met à jour le style de la section Hero
    Input("country", "value")       # Surveille les changements dans le Dropdown
)
def update_background_image(selected_country):
    # Chemin de l'image basé sur le pays sélectionné
    image_path = f"/static/Wallpapers/{selected_country}.jpg"
    # Retourne un style CSS pour définir l'image en fond
    return {
        "backgroundImage": f"url({image_path})",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "height": "100vh",  # Ajuste la hauteur pour couvrir l'écran
        "width": "100%"
    }


# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
