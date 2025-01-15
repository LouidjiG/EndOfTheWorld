from .fetch_air_quality_data import get_WAQI_air_quality_data
from .fetch_health_related_data import (
    fetch_health_personnel_data, 
    fetch_death_by_disease_data, 
    fetch_HIV_related_death_data,
    get_critical_medical_population
)
from .fetch_lifespan_data import fetch_lifespan_data
from .fetch_natural_disaster_data import get_natural_disaster_occurence

import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# #---- Health Personnel Data ----#
# print('\n---- Health Personnel Data ----')
# df_health_personnel = fetch_health_personnel_data('FRA')
# df_health_personnel = df_health_personnel[df_health_personnel['TimeDim'] == df_health_personnel['TimeDim'].max()]['NumericValue'].values[0]
# print(df_health_personnel)

# #---- Death by Disease Data ----#
# print('\n---- Death by Disease Data ----')
# df_death_disease = fetch_death_by_disease_data('FRA')
# df_death_disease = df_death_disease[df_death_disease['TimeDim'] == df_death_disease['TimeDim'].max()]
# df_death_disease = df_death_disease['NumericValue'].values[0]
# print(df_death_disease)

# #---- HIV Related Death Data ----#
# print('\n---- HIV Related Death Data ----')
# df_HIV_related_death = fetch_HIV_related_death_data('FRA')
# df_HIV_related_death = df_HIV_related_death[df_HIV_related_death['TimeDim'] == df_HIV_related_death['TimeDim'].max()]['NumericValue'].values[0]
# print(df_HIV_related_death)

# #---- Lifespan Data ----#
# print('\n---- Lifespan Data ----')
# df_lifespan = fetch_lifespan_data('FRA')
# df_lifespan = df_lifespan[df_lifespan['TimeDim'] == df_lifespan['TimeDim'].max()]
# df_lifespan = df_lifespan[df_lifespan['Dim1'] == 'SEX_BTSX']['NumericValue'].values[0]
# print(df_lifespan)

# #---- Air Quality Data ----#
# print('\n---- Air Quality Data ----')
# df_air_quality = get_WAQI_air_quality_data('FRA')['aqi'].values[0]
# print(df_air_quality)

def calculate_doomsday_year(country):
    """Calculates the doomsday year for a given country

    Args:
        country (string): Country ISO 3166-1 alpha-3 code

    Returns:
        int: doomsday year
    """
    country_Iso = {
        'FRA': 'France', 
        'ITA': 'Italy', 
        'CHN': 'China', 
        'MDG': 'Madagascar', 
        'RUS': 'Russia', 
        'TGO': 'Togo', 
        'KOR': 'South Korea', 
        'VNM': 'Vietnam', 
        'DZA': 'Algeria', 
        'BFA': 'Burkina Faso', 
        'MUS': 'Mauritius', 
        'LBN': 'Lebanon', 
        'MAR': 'Morocco'
        }

    health_personnel = fetch_health_personnel_data(country)
    health_personnel = health_personnel[health_personnel['TimeDim'] == health_personnel['TimeDim'].max()]['NumericValue'].values[0]

    air_quality = get_WAQI_air_quality_data(country)
    air_quality = air_quality['aqi'].values[0]

    death_disease = fetch_death_by_disease_data(country)
    death_disease = death_disease[death_disease['TimeDim'] == death_disease['TimeDim'].max()]
    death_disease = death_disease['NumericValue'].values[0]

    disaster_occurence = get_natural_disaster_occurence(country_Iso[country])

    weights = {
        "health_personnel": 0.3,
        "death_disease": 0.3,
        "natural_disaster_frequency": 0.3,
        "air_quality": 0.1,
    }
    critical_air_quality = 200
    critical_health_personnel = get_critical_medical_population(country_Iso[country])
    critical_death_disease = 50
    Drakes_equation_value = 151515

    health_personnel_score = min(critical_health_personnel/health_personnel,1)
    air_quality_score = min(1, air_quality/critical_air_quality)
    death_disease_score = min(1, death_disease/critical_death_disease)
    disaster_occurence_score = min(1, disaster_occurence/100)

    overall_score = weights["health_personnel"] * health_personnel_score + weights["death_disease"] * death_disease_score + weights["natural_disaster_frequency"] * disaster_occurence_score + weights["air_quality"] * air_quality_score

    # Probability to live multiplied by the number of years left. It gives the doomsday year with our modern problems.
    doomsday_year = int((1-overall_score) * Drakes_equation_value)
    return doomsday_year 

def calculate_time_left(doomsday_year):
    """Calculates the time left until the doomsday year

    Args:
        doomsday_year (int): doomsday year

    Returns:
        dict: dictionary with the following keys: years, months, days, hours, minutes, seconds
    """
    current_date = datetime.now()
    years_left = doomsday_year - current_date.year
    months_left = 12 - current_date.month
    days_left = 31 - current_date.day
    hours_left = 24 - current_date.hour
    minutes_left = 60 - current_date.minute
    seconds_left = 60 - current_date.second


    return {
        "years": years_left,
        "months": months_left,
        "days": days_left,
        "hours": hours_left,
        "minutes": minutes_left,
        "seconds": seconds_left
    }

# #---- Doomsday Year Calculation ----#
# print('\n---- Doomsday Year Calculation ----')
# for country in ['FRA', 'ITA', 'MDG', 'RUS', 'TGO', 'KOR', 'VNM', 'DZA', 'BFA', 'MUS', 'LBN', 'MAR']:
#      print(f"\n---- {country} ----")
#      doomsday_year = calculate_doomsday_year(country)
#      print(f"{country}: {doomsday_year}")




