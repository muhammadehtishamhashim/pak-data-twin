# Minimal working main.py for Pakistan Data Twin Dashboard

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Simple imports
from src.data_loader import load_all_data
from src.config import DASHBOARD_INDICATORS

def main():
    """Minimal main function"""
    
    st.set_page_config(
        page_title="Pakistan Data Twin Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Pakistan Data Twin Dashboard")
    st.write("✅ Minimal version running successfully!")
    
    # Load data
    try:
        data_dict = load_all_data()
        
        if data_dict:
            st.success(f"✅ Data loaded! Found {len(data_dict)} datasets.")
            
            # Simple charts
            for category in DASHBOARD_INDICATORS:
                df = data_dict.get(category)
                if df is not None and not df.empty:
                    st.subheader(f"{category} Data")
                    fig = px.line(df, x='Year', y='Value', title=f'{category} Over Time')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()