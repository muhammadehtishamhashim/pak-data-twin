#!/usr/bin/env python3
"""
Main entry point for Streamlit Cloud deployment - Pakistan Data Twin Dashboard
"""

import streamlit as st
import sys
import os

# Configure the page first (must be the first Streamlit command)
st.set_page_config(
    page_title="Pakistan Data Twin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    # Try to import and run the main application
    from src.app.main import main
    main()
    
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.info("Falling back to simple dashboard...")
    
    # Simple fallback dashboard
    import pandas as pd
    import plotly.express as px
    
    st.title("📊 Pakistan Data Twin Dashboard")
    st.caption("Simplified version - Import issues detected")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Year': list(range(2000, 2025)),
        'GDP': [100 + i*5 + (i%3)*10 for i in range(25)],
        'Education': [60 + i*0.8 for i in range(25)],
        'Internet': [1 + i*1.2 for i in range(25)]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.area(sample_data, x='Year', y='GDP', title='GDP Growth (Sample Data)')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.line(sample_data, x='Year', y=['Education', 'Internet'], 
                      title='Social Indicators (Sample Data)')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.warning("This is a fallback version. Check the application logs for import issues.")
    
except Exception as e:
    st.error(f"Application Error: {str(e)}")
    st.code(f"Error details: {type(e).__name__}: {str(e)}")
    
    # Show debug info
    st.subheader("Debug Information")
    st.write(f"Python version: {sys.version}")
    st.write(f"Working directory: {os.getcwd()}")
    st.write(f"Project root: {PROJECT_ROOT}")
    
    # List files in current directory
    try:
        files = os.listdir('.')
        st.write("Files in root directory:", files[:10])  # Show first 10 files
    except:
        st.write("Could not list directory contents")