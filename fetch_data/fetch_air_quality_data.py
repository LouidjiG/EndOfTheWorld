import pandas as pd
import requests
import plotly.express as px
# WAQI aire quality token: 21abc0384d5f519b7a35d9c75293845ddb4e8a23

def get_WAQI_air_quality_data(country):
    """Fetches air quality data for a given city

    Args:
        city (string): name of the country or ISI 3166-1 alpha-3 country code

    Returns:
        dataframe: dataframe with the following columns: aqi, dominentpol
            aqi (int): air quality index, the greater the worse
            dominentpol (string): dominent pollutant
    """
    token = '21abc0384d5f519b7a35d9c75293845ddb4e8a23'
    url = f'https://api.waqi.info/feed/{country}/?token={token}'
    response = requests.get(url)
    response = response.json()
    relevant_data  = ['aqi', 'dominentpol']
    df = pd.json_normalize(response['data'])
    return df[relevant_data]

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
    fig = px.bar(df, x='country', y='aqi', color='dominentpol',
                 title='Air Quality Index by Country', 
                 labels={'aqi': 'Air Quality Index', 'country': 'Country'})
    fig.show()


# Example usage
########## GOT A PROBLEM HERE WITH MOROCCO ##########
countries3 = ['france', 'italia', 'china', 'madagascar', 'russia', 'togo',
              'south korea', 'vietnam', 'algeria', 'burkina faso', 'MUS',
              'lebanon']


visualize_air_quality(countries3)