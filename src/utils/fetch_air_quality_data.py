import pandas as pd
import requests
import plotly.express as px
import os
import json
# WAQI aire quality token: 21abc0384d5f519b7a35d9c75293845ddb4e8a23
countries3 = {'FRA':'france', 'ITA': 'italia', 'CHN': 'china', 'MDG': 'madagascar', 'RUS': 'russia',
              'TGO': 'togo', 'KOR': 'south korea', 'VNM': 'vietnam', 'DZA': 'algeria', 'BFA': 'burkina faso', 
              'MUS': 'MUS', 'LBN': 'lebanon'}
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')


def save_WAQI_air_quality_data():
    """Fetches air quality data for all countries and saves it to a JSON file."""
    all_data = {}
    token = '21abc0384d5f519b7a35d9c75293845ddb4e8a23'
    
    for country_code, country_name in countries3.items():
        url = f'https://api.waqi.info/feed/{country_code}/?token={token}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()['data']
                all_data[country_code] = response_data
            else:
                print(f"Failed to fetch data")
                return None
        except requests.RequestException as e:
            print(f"An error occurred")
            return None
    
    filename = 'air_quality_data_all_countries.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(all_data, f)
    
    return all_data
    
def load_initial_data():
    global AIR_QUALITY
    AIR_QUALITY = save_WAQI_air_quality_data()

load_initial_data()

def get_WAQI_air_quality_data(country):
    """Fetches air quality data for a given country. If no data is found, returns default values.
    aqi = 45, dominentpol = "unknown"

    Args:
        country (string): name of the country or ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: dataframe with the following columns: aqi, dominentpol
    """
    filename = 'air_quality_data_all_countries.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    if not AIR_QUALITY:
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        data = AIR_QUALITY

    country_data = data.get(country, {})
    if isinstance(country_data, str):
        aqi = 45
        dominentpol = "unknown"
    else:
        if not country_data:
            raise ValueError(f"No data found for country: {country}")

        aqi = country_data.get('aqi', 45)
        dominentpol = country_data.get('dominentpol', "unknown")

    df = pd.DataFrame({'country': [country], 'aqi': [aqi], 'dominentpol': [dominentpol]})

    return df



def visualize_air_quality(list_of_countries):
    """Visualizes air quality data on a map using Plotly

    Args:
        list_of_countries (list): list of countries
    """
    data = []

    for country in list_of_countries:
        try:
            air_quality_data = get_WAQI_air_quality_data(country)
            air_quality_data['country'] = country
            data.append(air_quality_data)
        except:
            print(f'no data for {country}, please check the country name or ISO code')
    
    df = pd.concat(data)
    fig = px.bar(
        df, 
        x='country',
        y='aqi', 
        color='dominentpol',
        height=500,
        title='Air Quality Index by Country', 
        labels={'aqi': 'Air Quality Index', 'country': 'Country'},
        hover_data=['aqi', 'dominentpol']
    )
    fig.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),
        title_x=0.5,
        title_y=0.98,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    return fig


# Example usage
########## GOT A PROBLEM HERE WITH MOROCCO ##########

# visualize_air_quality(countries3)