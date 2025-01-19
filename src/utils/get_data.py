# On n'utilise jamais ce fichier car on veut cibler chaque pays et chaque type donnée dans notre projet. 
# On pourrait cependant l'utiliser pour afficher un tableau contenant l'ensemble de nos données pour chaque pays et une colonne en plus avec le nombre d'années avant la fin de ce pays

from .fetch_air_quality_data import get_WAQI_air_quality_data
from .fetch_health_related_data import (
    fetch_health_personnel_data,
    fetch_death_by_disease_data,
    fetch_HIV_related_death_data,
)
from .fetch_lifespan_data import fetch_lifespan_data
from .GlobalLandTemperatures import load_global_land_temperatures


def fetch_air_quality(country_code):
    """Wrapper pour récupérer les données de qualité de l'air."""
    return get_WAQI_air_quality_data(country_code)


def fetch_all_data_for_country(country_code):
    """
    Récupère toutes les données pour un pays donné via son code ISO.

    Args:
        country_code (str): Le code ISO du pays.

    Returns:
        dict: Dictionnaire contenant les données pour ce pays.
    """
    return {
        "air_quality": fetch_air_quality(country_code),
        "health_personnel": fetch_health_personnel_data(country_code),
        "death_by_disease": fetch_death_by_disease_data(country_code),
        "HIV_related_deaths": fetch_HIV_related_death_data(country_code),
        "lifespan": fetch_lifespan_data(country_code),
        "land_temperatures": load_global_land_temperatures(country_code),
    }


def fetch_all_countries_data(country_codes):
    """
    Récupère les données pour plusieurs pays et les organise dans un dictionnaire.

    Args:
        country_codes (list): Liste des codes ISO des pays.

    Returns:
        dict: Dictionnaire contenant les données pour chaque pays.
    """
    return {
        code: fetch_all_data_for_country(code)
        for code in country_codes
    }



