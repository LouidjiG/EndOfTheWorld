from .fetch_air_quality_data import get_WAQI_air_quality_data
from .fetch_health_related_data import (
    fetch_health_personnel_data,
    fetch_death_by_disease_data,
    fetch_HIV_related_death_data
)
from .fetch_lifespan_data import fetch_lifespan_data

__all__ = [
    'get_WAQI_air_quality_data',
    'fetch_health_personnel_data',
    'fetch_death_by_disease_data',
    'fetch_HIV_related_death_data',
    'fetch_lifespan_data'
]