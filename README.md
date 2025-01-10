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