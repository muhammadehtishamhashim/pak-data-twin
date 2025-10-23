# src/data_loader.py

import streamlit as st
import pandas as pd
from typing import Dict, List
# Import from sister module in src/
from src.config import DATA_PATH, CATEGORY_MAPPING

def _melt_data(df: pd.DataFrame, year_cols: List[str]) -> pd.DataFrame:
    """Helper function to transform wide-format data to long-format."""
    
    if not all(col in df.columns for col in ['Country Name', 'Indicator Name'] + year_cols):
        return pd.DataFrame()
        
    df_long = df.melt(
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
        value_vars=year_cols,
        var_name='Year',
        value_name='Value'
    )
    
    # Robust numeric conversion: handles non-numeric values gracefully
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce').astype('Int64')
    df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
    
    df_long.dropna(subset=['Year', 'Value'], inplace=True)
    
    return df_long

@st.cache_data
def load_all_data() -> Dict[str, pd.DataFrame]:
    """Loads, melts, and caches all required datasets."""
    all_data = {}
    
    unique_files = {v['file']: [] for v in CATEGORY_MAPPING.values()}
    for k, v in CATEGORY_MAPPING.items():
        unique_files[v['file']].append(k)

    for file_name, categories in unique_files.items():
        file_path = DATA_PATH / file_name
        try:
            df_raw = pd.read_csv(file_path, header=0) 
            year_cols = [col for col in df_raw.columns if str(col).isdigit() and len(str(col)) == 4 and int(col) >= 2000]

            df_long = _melt_data(df_raw, year_cols)
            
            if df_long.empty:
                 st.warning(f"Failed to process data for {file_name}. Check file structure and numeric values.")
                 continue

            for category in categories:
                all_data[category] = df_long.copy()
            
        except FileNotFoundError:
            st.error(f"Data file not found: {file_name}. Ensure it is in the data_processed/ folder.")
        except Exception as e:
            st.error(f"An unexpected error occurred processing {file_name}: {e}")
            
    return all_data
