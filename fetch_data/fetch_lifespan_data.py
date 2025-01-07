# https://ghoapi.azureedge.net/api/Dimension

import requests
import pandas as pd
import plotly.express as px

# List of ISO 3166-1 alpha-3 country codes used for this project
ISO3166_codes = ['FRA', 'ITA', 'CHN', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN', 'MAR']

def fetch_lifespan_data(country):
    """Fetches global health data for a given country

    Args:
        country (string): ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: panda dataframe with the following columns: TimeDim, Dim1, Value, NumericValue, Low, High
            TimeDim (string): year
            Dim1 (string): Sex indicator
            NumericValue (float): health indicator value as a float
    """    
    url = f"https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq '{country}'"
    response = requests.get(url)
    response = response.json()
    df = pd.json_normalize(response['value'])
    relevent_columns = ['TimeDim', 'Dim1', 'NumericValue']
    return df[relevent_columns]

def get_lastest_lifespan_data(country):
    """Fetches and processes global health data

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

    # Visualize the data using Plotly
    fig = px.bar(all_data, x='country', y='NumericValue', color='Dim1', barmode='group',
                title=f'Global Health Data by Country and Year {year}')
    fig.show()

# Example usage
# show_lastest_lifespan_data(ISO3166_code)
show_lifespan_data_by_year(ISO3166_codes, 2020)