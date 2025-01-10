import pandas as pd
from gdacs.api import GDACSAPIReader
import plotly.express as px

def fetch_natural_disaster_data(limit=100):
    """Fetches natural disaster data from the GDACS API

    Returns:
        event: natural disaster data
    """
    client = GDACSAPIReader()
    events = client.latest_events(limit=limit)
    return events

def process_natural_disaster_data(events):
    """Processes natural disaster data
    Note: in the rturned dataframe, the event_type column contains the type of the event 
    (e.g. EQ=earthquake, TC=tropical cyclone, FL=flood, VO=volcano, WF=wild fire, DR=drought, 
    TS=tsunami, SS=storm surge, LG=landslide, OT=other)
    
    Args:
        events (event): natural disaster data

    Returns:
        dataframe: panda dataframe with the following columns: 
        event_type, event_name, description, alert_level, country, fromdate, todate, latitude, longitude, severity
    """
    relevant_data = []
    for feature in events.features:
        properties = feature['properties']
        geometry = feature['geometry']
        relevant_data.append({
            'event_type': properties['eventtype'],
            'event_name': properties['eventname'],
            'description': properties['description'],
            'alert_level': properties['alertlevel'],
            'country': properties['country'],
            'fromdate': pd.to_datetime(properties['fromdate']),
            'todate': pd.to_datetime(properties['todate']),
            'latitude': geometry['coordinates'][1],
            'longitude': geometry['coordinates'][0],
            'severity': properties['severitydata']['severity']
        })
    return pd.DataFrame(relevant_data)

def get_natural_disaster_data(limit=100):
    """Fetches and processes natural disaster data

    Returns:
        dataframe: panda dataframe with the following columns: 
        event_type, event_name, description, alert_level, country, fromdate, todate, latitude, longitude, severity
    """
    events = fetch_natural_disaster_data(limit=limit)
    return process_natural_disaster_data(events)

import plotly.express as px


def visualize_natural_disaster_data(df):
    """Visualizes natural disaster data on a map using Plotly

    Args:
        df (pd.DataFrame): DataFrame containing natural disaster data
    """
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="event_name",
        hover_data=["event_type", "description", "alert_level", "country", "fromdate", "todate", "severity"],
        color="event_type",
        size='severity',
        size_max=20,
        zoom=1,
        height=600
    )
    fig.update_traces(marker_sizemin=5)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def get_natural_disaster_occurence(country, limit=100):
    """Get the number of natural disasters that occured in a country for the past N events

    Args:
        country (string): country name, e.g. 'France'
        limit (int, optional): limit of number of events studied. Defaults to 100.

    Returns:
        int: number of occurence of disasters in the given country
    """
    natural_disaster_data = get_natural_disaster_data(limit)
    natural_disaster_data = natural_disaster_data[natural_disaster_data['country'] == country].shape[0]
    return natural_disaster_data
    

# Example usage
# natural_disaster_data = get_natural_disaster_data(100)
# visualize_natural_disaster_data(natural_disaster_data)
# print(get_natural_disaster_occurence('Sudan', 100))

