import pandas as pd
import os
import plotly.express as px

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
CLEAN_DATA_DIR = os.path.join(DATA_DIR, 'clean')

countries = ["France", "Italy", "China", "Madagascar", "Russia", "Togo", "South Korea", "Vietnam", "Algeria", "Burkina Faso", "Mauritius", "Lebanon"]

def get_global_land_temperatures():
    """Reads the GlobalLandTemperaturesByCountry.csv and returns a DataFrame"""
    csv_path = os.path.join(RAW_DATA_DIR, 'GlobalLandTemperaturesByCountry.csv')
    df = pd.read_csv(csv_path)
    return df

def process_global_land_temperatures(df):
    """Processes the GlobalLandTemperaturesByCountry data"""
    countries = ["France", "Italy", "China", "Madagascar", "Russia", "Togo", "South Korea", "Vietnam", "Algeria", "Burkina Faso", "Mauritius", "Lebanon"]
    df = df[df['Country'].isin(countries)]
    
    df['dt'] = pd.to_datetime(df['dt'])
    df = df.sort_values(by=['Country', 'dt'])
    
    df['AverageTemperature'] = df.groupby('Country')['AverageTemperature'].fillna(method='ffill')
    
    df['Year'] = df['dt'].dt.year
    df = df.drop(columns=['dt'])
    df = df.drop(columns=['AverageTemperatureUncertainty'])
    
    yearly_df = df.groupby(['Country', 'Year']).mean().reset_index()
    
    return yearly_df

def save_global_land_temperatures(df):
    """Saves the processed GlobalLandTemperaturesByCountry data"""
    filename = 'global_land_temperatures.csv'
    filepath = os.path.join(CLEAN_DATA_DIR, filename)
    df.to_csv(filepath, index=False)

def load_global_land_temperatures():
    """Loads the processed GlobalLandTemperaturesByCountry data"""
    filename = 'global_land_temperatures.csv'
    filepath = os.path.join(CLEAN_DATA_DIR, filename)
    df = pd.read_csv(filepath)
    return df

def visualize_global_land_temperatures():
    """Visualizes global land temperatures using Plotly"""
    df = load_global_land_temperatures()
    fig = px.line(df, x='Year', y='AverageTemperature', color='Country')
    return fig

# df = get_global_land_temperatures()
# df = process_global_land_temperatures(df)
# save_global_land_temperatures(df)
# print("Global Land Temperatures data processed and saved")
# print(load_global_land_temperatures())
# fig = visualize_global_land_temperatures()
# fig.show()