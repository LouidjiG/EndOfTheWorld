import os
import json
import pandas as pd
import requests
import plotly.express as px

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
cached_data = {}

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def get_cache_filename(starttime, endtime, minmagnitude, maxmagnitude):
    """Generate a unique filename for caching"""
    return f"eq_data_{starttime}_{endtime}_{minmagnitude}_{maxmagnitude}.json"

def fetch_earthquake_data(starttime, endtime, minmagnitude=0, maxmagnitude=10):
    """Fetches earthquake data from the USGS API and saves to JSON"""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": minmagnitude,
        "maxmagnitude": maxmagnitude
    }
    
    filename = get_cache_filename(starttime, endtime, minmagnitude, maxmagnitude)
    filepath = os.path.join(RAW_DATA_DIR, filename)
    
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to decode JSON. Response content: {response.text}")
        raise
    
    with open(filepath, 'w') as f:
        json.dump(data, f)
    
    return data

def load_cached_data(starttime, endtime, minmagnitude=0, maxmagnitude=10):
    """Load data from cache or fetch if not exists"""
    filename = get_cache_filename(starttime, endtime, minmagnitude, maxmagnitude)
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return fetch_earthquake_data(starttime, endtime, minmagnitude, maxmagnitude)

def process_earthquake_data(data):
    """Processes earthquake data"""
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
    """Fetches and processes earthquake data"""
    cache_key = f"{starttime}_{endtime}_{minmagnitude}_{maxmagnitude}"
    
    # I could do this like the others by checking if the file exist but this methode seems not bad.
    # I will keep it like this.
    if cache_key not in cached_data:
        data = load_cached_data(starttime, endtime, minmagnitude, maxmagnitude)
        cached_data[cache_key] = process_earthquake_data(data)
    
    return cached_data[cache_key]

def visualize_earthquake_data():
    """Visualizes earthquake data on a map using Plotly

    Args:
        df (pd.DataFrame): DataFrame containing earthquake data
    """
    starttime = "2024-12-01"
    endtime = "2025-01-01"
    df = get_earthquake_data(starttime, endtime, 1, 10)
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
        height=500,
        title=f"Earthquakes from {starttime} to {endtime}"
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(
            margin={"r":0,"t":50,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title="Magnitude",
                tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                ticktext=[str(i) for i in range(1, 11)]
            ),
            title_x=0.5,
            title_y=0.98
        )

    return fig

# Example usage
# starttime = '2021-01-01'
# endtime = '2021-01-10'
# earthquake_data = get_earthquake_data(starttime, endtime, 1, 10)
# visualize_earthquake_data().show()