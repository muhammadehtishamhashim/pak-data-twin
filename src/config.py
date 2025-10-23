# src/config.py

from pathlib import Path

# Path to the project root (pak-data-twin) is two levels up from src/config.py
# Path to data_processed is one level up from src (i.e., pak-data-twin) then into data_processed
DATA_PATH = Path(__file__).resolve().parent.parent / 'data_processed'

# --- DATA MAPPING AND METADATA ---
CATEGORY_MAPPING = {
    'GDP': {
        'file': 'Pakistan_GDP.csv', 
        'indicator_name': 'GDP (current US$)', 
        'y_axis': 'Value (USD)', 
        'description': 'Pakistan\'s Annual Gross Domestic Product (GDP) in Current US$.'
    },
    'Education': {
        'file': 'Pakistan_School_Enrollment.csv', 
        'indicator_name': 'School enrollment, primary (% gross)', 
        'y_axis': 'Value (% Gross)', 
        'description': 'Gross Enrollment Ratio in Primary Education.'
    },
    'Health': { 
        'file': 'Pakistan_Net_User.csv', 
        'indicator_name': 'Individuals using the Internet (% of population)', 
        'y_axis': 'Value (%)', 
        'description': 'Digital Penetration (used as Health proxy).'
    },
    'Energy': { 
        'file': 'Pakistan_GDP.csv', 
        'indicator_name': 'GDP (current US$)', 
        'y_axis': 'Value (USD)', 
        'description': 'TEMPORARY: Showing GDP as an Energy proxy.'
    },
}

DASHBOARD_INDICATORS = ['GDP', 'Education', 'Health']
FORECASTING_INDICATORS = list(CATEGORY_MAPPING.keys())
