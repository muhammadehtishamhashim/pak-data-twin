#!/usr/bin/env python3
"""
Simplified main.py that should definitely work
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    """Simple main function that should work"""
    
    st.set_page_config(
        page_title="Pakistan Data Twin Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Pakistan Data Twin Dashboard")
    st.write("✅ App is running successfully!")
    
    # Try to load data
    try:
        from src.data_loader import load_all_data
        data_dict = load_all_data()
        
        if data_dict:
            st.success(f"✅ Data loaded successfully! Found {len(data_dict)} datasets.")
            
            # Show a simple chart
            for category, df in data_dict.items():
                if not df.empty:
                    st.subheader(f"{category} Data")
                    fig = px.line(df, x='Year', y='Value', title=f'{category} Over Time')
                    st.plotly_chart(fig, use_container_width=True)
                    break  # Just show one chart for testing
        else:
            st.warning("No data loaded")
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        
        # Show sample data instead
        sample_data = pd.DataFrame({
            'Year': list(range(2000, 2025)),
            'Value': [100 + i*5 for i in range(25)]
        })
        
        fig = px.line(sample_data, x='Year', y='Value', title='Sample Data')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()