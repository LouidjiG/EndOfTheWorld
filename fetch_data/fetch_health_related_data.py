import requests
import pandas as pd

def fetch_HIV_related_death_data(country, year=None):
    """Number of people dying from HIV-related causes

    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means the latest year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    url = f"https://ghoapi.azureedge.net/api/HIV_0000000006"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            print("Data fetched successfully")
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
            if year:
                return df[(df['SpatialDim'] == country)][(df['TimeDim'] == year)]
            else:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == df['TimeDim'].max())]
                return df

        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def fetch_health_personnel_data(country, year=None):
    """Number of health personnel (per 10 000 population)
    Args:
        country (string): country ISO 3166-1 alpha-3 code
        year (int, optional): year. Defaults to None, which means the latest year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    url = f"https://ghoapi.azureedge.net/api/HWF_0003"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            print("Data fetched successfully")
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
            if year:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == year)]
                return df
            else:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == df['TimeDim'].max())]
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
        year (int, optional): year. Defaults to None, which means the latest year.

    Returns:
        dataframe: panda dataframe with the following columns: SpatialDim, TimeDim, NumericValue
    """
    url = f"https://ghoapi.azureedge.net/api/NCDMORT3070"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            print("Data fetched successfully")
            relevent_columns = ['SpatialDim', 'TimeDim', 'NumericValue']
            df = pd.json_normalize(response['value'])[relevent_columns]
            df = df.dropna()
            if year:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == year)]
                return df
            else:
                df = df[(df['SpatialDim'] == country)]
                df = df[(df['TimeDim'] == df['TimeDim'].max())]
                df = df[(df['NumericValue'] == df['NumericValue'].max())]
                return df

        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

print(fetch_HIV_related_death_data('FRA'))
print(fetch_health_personnel_data('FRA'))
print(fetch_death_by_disease_data('FRA'))

#SA_0000001807 cancer age standardized rate per 100k
# WHS2_160 mortality by cause cancer
# NCDMORT3070 death by cancer, cardiovascular diseases, diabetes or chronic respiratory diseases