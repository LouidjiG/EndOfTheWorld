import requests
import pandas as pd
import numpy as np
import plotly.express as px

def fetch_HIV_related_death_data(country, year=None):
    """Number of people dying from HIV-related causes

    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means every possible year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    url = f"https://ghoapi.azureedge.net/api/HIV_0000000006"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
            if year:
                return df[(df['SpatialDim'] == country)][(df['TimeDim'] == year)]
            else:
                if df[(df['SpatialDim'] == country)].size == 0:
                    return pd.DataFrame({'SpatialDim': [country], 'TimeDim': [0], 'NumericValue': [df['NumericValue'].mean()]})
                df = df[(df['SpatialDim'] == country)]
                return df
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_population(country):
    """Get the population of a country

    Args:
        country (string): country name

    Returns:
        dataframe: panda dataframe with today's and tomorrow's number of people in the given country.
    """
    url = f"https://d6wn6bmjj722w.population.io:443/1.0/population/{country}/today-and-tomorrow/"

    
    if country == 'Russia':
        return pd.DataFrame({'population': [145912025]})
    if country == 'South Korea':
        return pd.DataFrame({'population': [51780579]})
    if country == 'Burkina Faso':
        return pd.DataFrame({'population': [20903273]})
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            data = pd.json_normalize(response['total_population'][0])
            return data
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_critical_medical_population(country):  
    """Get the critical number of medical personnel needed for a country

    Args:
        country (string): country name

    Returns:
        int: number of medical personnel needed
    """
    pop = get_population(country)['population'].values[0]
    return int(np.ceil(pop * 0.002))
    


def fetch_health_personnel_data(country, year=None):
    """Generalist medical practitioners (number) f, there is no data for the health personnel in a country,
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
    url = f"https://ghoapi.azureedge.net/api/HWF_0003"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
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

            
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
        
def fetch_death_by_disease_data(country, year=None):
    """Probability (%) of dying between age 30 and exact age 70 from any of cardiovascular disease, cancer, diabetes, or chronic respiratory disease"
    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means every possible year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    url = f"https://ghoapi.azureedge.net/api/NCDMORT3070"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
            if year:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == year)]
                return df
            else:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['NumericValue'] == df['NumericValue'].max())]
                return df

        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
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
    
    
# visualize_hiv_data().show()
# print(fetch_health_personnel_data('CHN'))
# print(get_population('South Korea'))
# print(get_critical_medical_population('RUS'))
# print(get_population('France'))

# visualize_death_desease_data().show()
# 1.0.PSev.Poor4uds
