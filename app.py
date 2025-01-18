import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import datetime
from src.utils.calculate_doomsday_year import calculate_doomsday_year
from src.utils.fetch_air_quality_data import visualize_air_quality
from src.utils.fetch_natural_disaster_data import visualize_natural_disaster_data
from src.utils.fetch_earthquake_data import visualize_earthquake_data
from src.utils.fetch_health_related_data import visualize_death_desease_data, visualize_health_personnel_data, visualize_hiv_data
from src.utils.fetch_lifespan_data import visualize_lifespan_data_by_year

doomsday_country_cache = {}

app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap",
    "/assets/style.css" 
])


country = {
    "France": "FRA", 
    "Italie": "ITA", 
    "Chine": "CHN", 
    "BurkinaFaso": "BFA",
    "Madagascar": "MDG", 
    "Tchétchénie": "RUS", 
    "Togo": "TGO", 
    "Corée": "KOR",
    "Vietnam": "VNM", 
    "Algérie": "DZA", 
    "Burkina Faso": "BFA", 
    "Maurice": "MUS", 
    "Liban": "LBN", 
    }

app.layout = html.Div([
    html.Section(className="heroSection", id="heroSection", children=[
        html.Div(className="backgroundImage first"),
        html.Div(className="backgroundImage second"),

        html.Div(className="counterContainer", children=[
            html.Div(className="remainingTimeContainer", children=[
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
                    ],
                    value="France",
                    className="countryDropdown",
                    clearable=False

                ),
            ]),
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
            interval=1000, 
            n_intervals=0,
        )
        
    ]),    

    # Section Map
    html.Section(className="map", children=[
        dcc.Dropdown(
            id="filter",
            options=[
                {"label": "Air Quality", "value": "air_quality"},
                {"label": "Earthquake", "value": "earthquake"},
                {"label": "Number of health personnel by country", "value": "health_personnel"},
                {"label": "lifespan by country", "value": "lifespan"},
                {"label": "HIV death", "value": "HIV"},
                {"label": "Proportion of death by disease", "value": "death_by_disease"},
            ],
            value="health",
            className="mapsDropdown",
            clearable=False
        ),
        html.Div(id="map-container", className="mapDiv")

    ]),

    html.Div(className="factTitle", children=[html.H3("EFFECTS")]),

    html.Section(className="importantFacts", children=[
        html.Div(className="fact", children=[
            html.H3("PREMATURED DEATHS"),
            html.P("79 884 002"),
            html.P("People")
            ]),
        html.Div(className="fact", children=[
            html.H3("LEAD IN THE BRAIN"),
            html.P("800"),
            html.P("Millions of childrens")
            ]),
        html.Div(className="fact", children=[
            html.H3("PLASTIC IN THE HUMAN BODY"),
            html.P("121 000"),
            html.P("Microplastic particles in the average human body")
            ]),
        html.Div(className="fact", children=[
            html.H3("LIFE EXPECTANCY DECREASE"),
            html.P("-6"),
            html.P("Years")
            ]),

    ]),
    # Section Facts Graphs
    html.Section(className="factsGraphs", children=[
        html.H3("IMPORTANT DETAILS"),
        html.Div(className="graph", children=[
            # TODO
            # QUALITE DE L'AIR
        ]),
        html.Div(className="graph", children=[
            # TODO
            # VIH
        ]),      
        html.Div(className="graph", children=[
            # TODO
            # TREMBLEMENTS DE TERRE
        ]),
        html.Div(className="graph", children=[
            # TODO
            # DESASTRES NATURELS
        ]),    
    ]),


    # Section Main Actors
    html.Section(className="mainActors", children=[
    html.H2("THEIR FAULT"),
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
            html.Textarea(placeholder="Give us your idea", id="idea"),
            html.Button("Send", type="submit", id="submit-button")  
        ])
    ]),

    # Footer
    html.Footer(children=[
        html.P("© Copyrights 2025")
    ])
])
@app.callback(
    Output("map-container", "children"),
    Input("filter", "value")
)
def update_map(selected_filter):
    if selected_filter == "air_quality":
        air_quality_fig = visualize_air_quality(country.values())
        return dcc.Graph(figure=air_quality_fig)
    elif selected_filter == "natural_disasters":
        # natural_disasters_fig = visualize_natural_disaster_data()
        return html.Div("")
    elif selected_filter == "earthquake":
        # HIV_fig = visualize_hiv_data()
        return html.Div("")
    elif selected_filter == "health_personnel":
        # HIV_fig = visualize_hiv_data()
        return html.Div("")
    elif selected_filter == "HIV":
        # HIV_fig = visualize_hiv_data()
        return html.Div("")
    elif selected_filter == "death_by_disease":
        # health_personnel_fig = visualize_health_personnel_data()
        return html.Div("")
    else:
        return html.Div("Select a filter to see the map")


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
