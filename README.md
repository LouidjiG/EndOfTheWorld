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

## the Model
Idea: We gather data on mortality rates by country for a specific year. We will cross-reference this data with greenhouse gas emissions by country, natural disaster datas and specifically earthquake datas.
As input, the user specifies their country (or continent), and we retrieve the environmental, social, and economic data for that location. We run the model, and boom—we get the year of death!

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