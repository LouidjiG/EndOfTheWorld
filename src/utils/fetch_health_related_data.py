import requests
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
# ------------------------------------------Load data------------------------------------------
def save_HIV_related_death_data():
    """Number of people dying from HIV-related causes

    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means every possible year.

    Returns:
        json: HIV-related death data in json format
    """
    url = "https://ghoapi.azureedge.net/api/HIV_0000000006"
    filename = "HIV_related_death_data.json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()['value']
            with open(os.path.join(RAW_DATA_DIR, filename), 'w') as f:
                json.dump(response, f)
            return response
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def save_health_personnel_data():
    """Generalist medical practitioners (number). Save the data in a json file in data\\raw folder

    Returns:
        json: health personnel data in json format
    """
    url = "https://ghoapi.azureedge.net/api/HWF_0003"
    filename = "health_personnel_data.json"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()['value']
            with open(os.path.join(RAW_DATA_DIR, filename), 'w') as f:
                json.dump(response, f)
            return response
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_death_by_disease_data():
    """Save datas in JSON format about: Probability (%) of dying between age 30 and exact age 70 
    from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease"

    Returns:
        json: death by disease data in json format
    """
    url = "https://ghoapi.azureedge.net/api/NCDMORT3070"
    filename= "death_by_disease_data.json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()['value']
            with open(os.path.join(RAW_DATA_DIR, filename), 'w') as f:
                json.dump(response, f)
            return response
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def load_initial_data():
    global DEATH_BY_DISEASE_DATA, HEALTH_PERSONNEL_DATA, HIV_DATA
    DEATH_BY_DISEASE_DATA = save_death_by_disease_data()
    HEALTH_PERSONNEL_DATA = save_health_personnel_data()
    HIV_DATA = save_HIV_related_death_data()

load_initial_data()
# ------------------------------------------Load data------------------------------------------

# ------------------------------------------Fetch data------------------------------------------
def fetch_HIV_related_death_data(country, year=None):
    """Fetch HIV-related death data for a country

    Args:
        country (_type_): _description_
        year (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    filename = 'HIV_related_death_data.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
    if not HIV_DATA:
        with open(filepath, 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data)[relevent_columns]
    else:
        df = pd.json_normalize(HIV_DATA)[relevent_columns]
    if year:
        return df[(df['SpatialDim'] == country)][(df['TimeDim'] == year)]
    else:
        if df[(df['SpatialDim'] == country)].size == 0:
            return pd.DataFrame({'SpatialDim': [country], 'TimeDim': [0], 'NumericValue': [df['NumericValue'].mean()]})
        df = df[(df['SpatialDim'] == country)]
        return df
        
def fetch_health_personnel_data(country, year=None):
    """Fetch health personnel data for a country. If there is no data for the health personnel in the country,
    We estimate the number of health personnel needed based on the number of death by a disease in the country.
    Here are the details of the estimation:
    estimation = Median * (alpha + beta/(percentageOfDyingPeople+gama)) 
    Median: median number of health personnel in the world
    alpha: A scaling factor (e.g. 0.5 adjusts the baseline number to half the global median for very high mortality rates).
    beta: A parameter to adjust the sensitivity of the estimation to the mortality rate (default value is 1).
    gama: Prevents extremely high results for countries with low mortality rates. (default value is 0.1)
    percentageOfDyingPeople: Probability (%) of dying between age 30 and exact age 70 some deseases.

    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means every possible year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    filename = 'health_personnel_data.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
    if not HEALTH_PERSONNEL_DATA:
        with open(filepath, 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data)[relevent_columns]
    else:
        df = pd.json_normalize(HEALTH_PERSONNEL_DATA)[relevent_columns]
    if year:
        df = df[(df['SpatialDim'] == country)]
        df = df[(df['TimeDim'] == year)]
        return df
    else:
        if df[(df['SpatialDim'] == country)].size == 0:
            percentageOfDying = 1/fetch_death_by_disease_data(country=country)['NumericValue'].values[0]
            median = df['NumericValue'].median()  
            alpha = 0.5
            beta = 1
            gama = 0.1
            estimation = median * (alpha + beta/(percentageOfDying+0.1))
            return pd.DataFrame({'SpatialDim': [country], 'TimeDim': [0], 'NumericValue': [estimation]})

        else: 
            df = df[(df['SpatialDim'] == country)]
        return df
    
def fetch_death_by_disease_data(country, year=None):
    """Fetch probability (%) of dying between age 30 and exact age 70 
    from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease for a country.

    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means every possible year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    filename = 'death_by_disease_data.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
    if not DEATH_BY_DISEASE_DATA:
        with open(filepath, 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data)[relevent_columns]
    else:
        df = pd.json_normalize(DEATH_BY_DISEASE_DATA)[relevent_columns]
    if year:
        df = df[(df['SpatialDim'] == country)]
        df = df[(df['TimeDim'] == year)]
        return df
    else:
        df = df[(df['SpatialDim'] == country)]
        df = df[(df['NumericValue'] == df['NumericValue'].max())]
        return df
# ------------------------------------------Fetch data------------------------------------------
    
# ---------------------------------------Visualize data-----------------------------------------
def visualize_hiv_data(countries=None):
    """Visualizes HIV-related deaths by country

    Args:
        countries (table, optional): countries to visualize. Defaults to None.

    Raises:
        ValueError: No data collected for any country

    Returns:
        fig: plotly figure
    """
    if countries is None:
        countries = ['FRA', 'ITA', 'CHN', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN']
    
    try:
        all_data = []
        for country in countries:
            df = fetch_HIV_related_death_data(country)
            if df is not None:
                # Get latest year data
                latest_year = df[df['TimeDim'] != 0]['TimeDim'].max()
                latest_data = df[df['TimeDim'] == latest_year]
                all_data.append(latest_data)
        
        if not all_data:
            raise ValueError("No data collected for any country")
            
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values('NumericValue', ascending=True)
        
        fig = px.bar(final_df,
                    x='NumericValue',
                    y='SpatialDim',
                    orientation='h',
                    title='HIV-related Deaths by Country (Latest Year)',
                    labels={'NumericValue': 'Number of Deaths',
                           'SpatialDim': 'Country'},
                    hover_data=['TimeDim'])
        
        fig.update_layout(showlegend=False)
        return fig
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None
    
    
def visualize_death_desease_data(countries=None):
    """Visualizes death by deseases by country

    Args:
        countries (table, optional): countries to visualize. Defaults to None.

    Raises:
        ValueError: No data collected for any country

    Returns:
        fig: plotly figure
    """
    if countries is None:
        countries = ['FRA', 'ITA', 'CHN', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN']
    
    try:
        all_data = []
        for country in countries:
            df = fetch_death_by_disease_data(country)
            if df is not None:
                # Get latest year data
                latest_year = df[df['TimeDim'] != 0]['TimeDim'].max()
                latest_data = df[df['TimeDim'] == latest_year]
                all_data.append(latest_data)
        
        if not all_data:
            raise ValueError("No data collected for any country")
            
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values('NumericValue', ascending=True)
        
        fig = px.bar(final_df,
                    x='NumericValue',
                    y='SpatialDim',
                    orientation='h',
                    title='Probability (%) of dying between age 30 and exact age 70 from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease (lastest year)',
                    labels={'NumericValue': 'percentage (%) of deaths',
                           'SpatialDim': 'Country'},
                    hover_data=['TimeDim'])
        
        fig.update_layout(showlegend=False)
        return fig
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None
    
def visualize_health_personnel_data(countries=None):
    """Visualizes health personnel by country

    Args:
        countries (table, optional): countries to visualize. Defaults to None.

    Raises:
        ValueError: No data collected for any country

    Returns:
        fig: plotly figure
    """
    if countries is None:
        countries = ['FRA', 'ITA', 'CHN', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN']
    
    try:
        all_data = []
        for country in countries:
            df = fetch_health_personnel_data(country)
            if df is not None:
                # Get latest year data
                latest_year = df[df['TimeDim'] != 0]['TimeDim'].max()
                latest_data = df[df['TimeDim'] == latest_year]
                all_data.append(latest_data)
        
        if not all_data:
            raise ValueError("No data collected for any country")
            
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values('NumericValue', ascending=True)
        
        fig = px.bar(final_df,
                    x='NumericValue',
                    y='SpatialDim',
                    orientation='h',
                    title='number of health personnel by country (lastest year)',
                    labels={'NumericValue': 'percentage (%) of deaths',
                           'SpatialDim': 'Country'},
                    hover_data=['TimeDim'])
        
        fig.update_layout(showlegend=False)
        return fig
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None
# ---------------------------------------Visualize data-----------------------------------------

# ---------------------------------------Population data----------------------------------------
def get_population(country):
    """Get the population for a given country

    Args:
        country (string): ISO 3166-1 alpha-3 country code

    Returns:
        dataframe: dataframe with the population number
    """
    filename = 'population_number.json'
    filepath = os.path.join(RAW_DATA_DIR, filename)

    with open(filepath, 'r') as file:
        data = json.load(file)

    population = data.get(country, None)
    if population is None:
        raise ValueError(f"No population data found for country: {country}")

    df = pd.DataFrame({'country': [country], 'population': [population]})
    return df

def get_critical_medical_population(country):  
    """Get the critical number of medical personnel needed for a country

    Args:
        country (string): country name

    Returns:
        int: number of medical personnel needed
    """
    pop = get_population(country)['population'].values[0]
    return int(np.ceil(pop * 0.002))

# print(fetch_death_by_disease_data('FRA'))
# print(fetch_health_personnel_data('FRA'))
# print(fetch_HIV_related_death_data('FRA'))