#!/usr/bin/env python3
"""
Simplified version of the Pakistan Data Twin Dashboard for testing
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Pakistan Data Twin Dashboard - Test",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Pakistan Data Twin Dashboard - Test Version")
    st.write("This is a simplified version to test deployment.")
    
    # Create some sample data
    sample_data = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024],
        'GDP': [100, 105, 110, 115, 120],
        'Education': [70, 72, 74, 76, 78]
    })
    
    # Simple chart
    fig = px.line(sample_data, x='Year', y='GDP', title='Sample GDP Chart')
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("✅ App is working! Python version and dependencies are compatible.")

if __name__ == "__main__":
    main()