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

5. Set up environment variables in the `.env` file.

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

- **Human Lifespan**:
  - [Global health data](https://ghoapi.azureedge.net/)

- **Natural disaster**
  - [Natural disaster](gdacs.api)
  
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

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