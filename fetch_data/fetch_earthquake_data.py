import requests
import pandas as pd
import plotly.express as px

def fetch_earthquake_data(starttime, endtime, minmagnitude=0, maxmagnitude=10):
    """Fetches earthquake data from the USGS API

    Args:
        starttime (string): date in the format 'YYYY-MM-DD'
        endtime (string): date in the format 'YYYY-MM-DD'
        minmagnitude (int, optional): minimum magnitude. Defaults to 0.
        maxmagnitude (int, optional): maximum magnitude. Defaults to 10.

    Returns:
        json: earthquake data in json format
    """
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": minmagnitude,
        "maxmagnitude": maxmagnitude
    }
    response = requests.get(url, params=params)
    return response.json()

def process_earthquake_data(data):
    """Processes earthquake data

    Args:
        data (json): earthquake data in json format

    Returns:
        dataframe: panda dataframe with the following columns: time, magnitude, depth, latitude, longitude, place
    """
    earthquakes = []
    for feature in data['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        lat, lon = geometry['coordinates'][1], geometry['coordinates'][0]
        earthquakes.append({
            'time': pd.to_datetime(properties['time'], unit='ms'),
            'magnitude': properties['mag'],
            'depth': geometry['coordinates'][2],
            'latitude': lat,
            'longitude': lon,
            'place': properties['place']
        })
    return pd.DataFrame(earthquakes)

def get_earthquake_data(starttime, endtime, minmagnitude=0, maxmagnitude=10):
    """Fetches and processes earthquake data

    Args:
        starttime (string): date in the format 'YYYY-MM-DD'
        endtime (string): date in the format 'YYYY-MM-DD'
        minmagnitude (int, optional): minimum magnitude. Defaults to 0.
        maxmagnitude (int, optional): maximum magnitude. Defaults to 10.

    Returns:
        dataframe: panda dataframe with the following columns: time, magnitude, depth, latitude, longitude, place
    """
    data = fetch_earthquake_data(starttime, endtime, minmagnitude, maxmagnitude)
    return process_earthquake_data(data)

def visualize_earthquake_data(df):
    """Visualizes earthquake data on a map using Plotly

    Args:
        df (pd.DataFrame): DataFrame containing earthquake data
    """
    # Add a size column for the marker size (see a greater difference between magnitudes)
    df['size'] = df['magnitude'] ** 2
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="place",
        hover_data=["time", "magnitude", "depth"],
        color="magnitude",
        size="magnitude",
        size_max=13,
        zoom=1,
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# Example usage
starttime = '2020-01-01'
endtime = '2021-01-10'
earthquake_data = get_earthquake_data(starttime, endtime, 5, 10)
visualize_earthquake_data(earthquake_data)