## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-backend-project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies: (navigate to the directory where the requirements.txt is located)
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the backend application, run:
```
python src/main.py
```

## APIs Used
- **Air Quality**: 
  - [World Air Pollution](http://waqi.info/)

- **Earthquake**:
  - [earthquake usgs gov](https://earthquake.usgs.gov/)

- **Human Lifespan and health realated data**:
  - [Global health data](https://ghoapi.azureedge.net/)

- **Natural disaster**
  - [Natural disaster](gdacs.api)

## the prediction
We will use datas about Air quality, Natural disaster, human LifeSpan and health related data to predict the end of the human civilisation in a given country. 
We use drakes equation to get a upper limit on the number of years befor the end of our civilisation. 
Drakes equation: N = R * f_p * n_e * f_l * f_i * f_c * L
             <=> L = N / (R * f_p * n_e * f_l * f_i * f_c )

N: Number of civilizations in the Milky Way galaxy with whom communication might be possible. (1: Assume we are currently the only detectable technological civilization.)
R: Rate of star formation in the galaxy (2: About 2 stars form per year in the Milky Way.)
f_p: Fraction of stars with planetary systems (0.5: Half of the stars have planetary systems.)
n_e: Average number of habitable planets per planetary system (0.2: Each planetary system has an average of 0.2 habitable planets.)
f_l: Fraction of habitable planets where life arises (0.33: One-third of habitable planets develop life.)
f_i: Fraction of planets with life where intelligent life evolves (0.01: 1% of planets with life develop intelligent life.)
f_c: Fraction of civilizations that develop detectable technologies (0.01: 1% of intelligent civilizations develop detectable technologies.)
L: Average lifespan of a technological civilization (what we want to estimate)

This equations gives us appriximately 151,515 years before the end of the human civilisation.

Our calculation:
We calculate a multiplier that will be between 0 and 1 based on the proportion of health personnel, the quality of the air, the death rate for some types of deseases, the occurence of some natural disaster and the lifespan. All of those datas are categorised by country. Here is a more precise way of how we calculate the multiplicator:
- health_personnel_score = min(critical number of health personnel / actual number of health personnel, 1)
- air_quality_score = min(1, actual air quality / critical air quality)
- death_disease_score = min(1, death rate / critical death rate)
- disaster_occurence_score = min(1, disaster occurence/100)
- lifespan_score = 1 if lifespan is over 70yo and 0 if not.

We then use weights for those value: 
weights = {
        "health_personnel": 0.2,
        "death_disease": 0.3,
        "natural_disaster_frequency": 0.2,
        "air_quality": 0.1,
        "lifespan": 0.2
    }
And calculate the overall score using those weights and values.
we then calculate the doomsday year by multiplying (1-overall_score) and the Drake's equation value.

list of country:
- France 
- Madagascar
- Togo
- Algérie
- Burkina Faso
- Italie
- Corée
- Vietnam
- Tchétchénie
- Maurice
- Chine
- Liban

## The Developer Guide

- **Architecture du projet**

Nous avons respecté l'architecture demandé dans le cahier des charges du projet :

EndOfTheWorld/
│
├── main.py                  # Main application file (entry point)
├── README.md                # Project overview and documentation
├── requirements.txt         # Python dependencies
│
├── assets/                  # Static assets and style resources
│   ├── style.css            # CSS file for styling the page
│   └── images/              # Folder containing country-specific background images
│       ├── France.jpg
│       ├── Japan.jpg
│       └── USA.jpg
│
├── data/raw/                # Raw data files in JSON format
│   ├── air_quality_data_all_countries.json
│   ├── death_by_disease_data.json
│   ├── eq_data_2021_01_01_2021-01-10_1_10.json
│   ├── health_personnel_data.json
│   ├── HIV_related_death_data.json
│   ├── lifespan_data.json
│   ├── natural_disaster_data_100.json
│   └── population_number.json
│
├── src/utils/               # Utilities for data fetching and calculations
│   ├── __init__.py
│   ├── calculate_doomsday_year.py
│   ├── fetch_air_quality_data.py
│   ├── fetch_earthquake_data.py
│   ├── fetch_health_related_data.py
│   ├── fetch_lifespan_data.py
│   └── fetch_natural_disaster_data.py


## Analysis Report

This project aims to analyze data to predict a potential "end of humanity" by identifying impactful events across various domains such as:

- Air quality
- Natural disasters
- Life expectancy
- And much more...

In the face of challenges posed by climate change, natural disasters, and other global issues, we must understand how these factors interact to assess their potential impact on humanity's future. We have collected and analyzed data from reliable sources, applied to predictions, to draw meaningful conclusions.

- **Air Quality**

Pollution levels highly increase, posing significant threats to both the environment and human health.

- **Seismic Activity**

We are seeing a growing number of significant earthquakes in certain regions over recent years compared to previous decades.

- **Public Health & Life Expectancy**

We can observe a decline in life expectancy in regions affected by conflicts or pandemics.

Certain contagious diseases, such as HIV, are spreading significantly in less developed countries.

- **Natural Disasters**

There is also an increase in the frequency of extreme weather events, such as hurricanes, floods, and more.

- **And What's the Conclusion?**

Current trends show that air quality and natural disasters are the most critical factors. CO2 levels are continuously rising, and we must find solutions to address this issue of air pollution.

We also need to strengthen infrastructures to withstand extreme weather events and work collectively to slow down the trends that are leading humanity toward a decline.

## Copyright 

We hereby declare, on our honor, that **the entirety of the code provided was crafted by us**, the result of relentless effort and extensive research into every available functionality. 

... Except for this message and the architecture below, of course – because, let’s face it, we couldn’t resist getting a little help to make this declaration as polished as possible. 😏


