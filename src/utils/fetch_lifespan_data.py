# https://ghoapi.azureedge.net/api/Dimension

import os
import json
import requests
import pandas as pd
import plotly.express as px

# List of ISO 3166-1 alpha-3 country codes used for this project
ISO3166_codes = ['FRA', 'ITA', 'CHN', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN', 'MAR']
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')

def save_lifespan_data():
    """Save Lifespan data for a given country to a JSON file

    Args:
        country (string): ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: panda dataframe with the following columns: TimeDim, Dim1, Value, NumericValue, Low, High
            TimeDim (string): year
            Dim1 (string): Sex indicator
            NumericValue (float): health indicator value as a float
    """    
    url = f"https://ghoapi.azureedge.net/api/WHOSIS_000001"
    filename = f'lifespan_data.json'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()['value'][0]
            with open(os.path.join(RAW_DATA_DIR, filename), 'w') as f:
                json.dump(response, f)
            return response
        else:
            print(f'Error fetching data')
            return None
    except:
        print(f'Error fetching data')
        return None
    
def load_lifespan_data():
    global LIFESPAN
    LIFESPAN = save_lifespan_data()

load_lifespan_data()
    
def fetch_lifespan_data(country, year=None):
    """Fetches Lifespan data for a given country

    Args:
        country (string): ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: panda dataframe with the following columns: TimeDim, Dim1, Value, NumericValue, Low, High
            TimeDim (string): year
    """
    filename = f'lifespan_data.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
    if not LIFESPAN:
        with open(filepath, 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data)[relevent_columns]
    else:
        df = pd.json_normalize(LIFESPAN)[relevent_columns]
    if year:
        return df[(df['SpatialDim'] == country)][(df['TimeDim'] == year)]
    else:
        if df[(df['SpatialDim'] == country)].size == 0:
            return pd.DataFrame({'SpatialDim': [country], 'TimeDim': [0], 'NumericValue': [df['NumericValue'].mean()]})
        df = df[(df['SpatialDim'] == country)]
        return df

def get_lastest_lifespan_data(country):
    """Fetches and processes lifespan data

    Args:
        country (string): ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: panda dataframe with the following columns: TimeDim, Dim1, Value, NumericValue, Low, High
            TimeDim (string): year
    """
    data = fetch_lifespan_data(country)
    return data[data['TimeDim'] == data['TimeDim'].max()]

def show_lastest_lifespan_data(countries):
    """Displays global health data for a given country

    Args:
        country (string): ISO 3166-1 alpha-3 country code
    """
    all_data = pd.DataFrame()
    for country in countries:
        latest_data = get_lastest_lifespan_data(country)
        latest_data['country'] = country
        all_data = pd.concat([all_data, latest_data])

    # Visualize the data using Plotly
    fig = px.bar(all_data, x='country', y='NumericValue', color='Dim1', barmode='group',
                title='Latest Global Health Data by Country and Sex')
    fig.show()

def show_lifespan_data_by_year(countries, year):
    """Displays global health data for a given country and year

    Args:
        country (string): ISO 3166-1 alpha-3 country code
        year (int): year
    """
    all_data = pd.DataFrame()
    for country in countries:
        data = fetch_lifespan_data(country)
        data = data[data['TimeDim'] == year]
        data['country'] = country
        all_data = pd.concat([all_data, data])

    fig = px.bar(all_data, x='country', y='NumericValue', color='Dim1', barmode='group',
                title=f'Global Health Data by Country and Year {year}')
    fig.show()

# Example usage
# show_lastest_lifespan_data(ISO3166_code)
# show_lifespan_data_by_year(ISO3166_codes, 2020)
# print(get_lastest_lifespan_data('FRA'))