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
- Marocain