#!/usr/bin/env python3
"""
Main entry point for Streamlit Cloud deployment - Pakistan Data Twin Dashboard
Fixed CORS and configuration issues
"""

import sys
import os

# Add project root to path for imports BEFORE any streamlit imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now import streamlit and other modules
import streamlit as st

def main():
    """Main application entry point with proper error handling"""
    
    # Configure the page first (must be the first Streamlit command)
    st.set_page_config(
        page_title="Pakistan Data Twin Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        # Import the components we need (avoiding the main() function to prevent double st.set_page_config)
        from src.app.main import render_dashboard, render_forecasting, PAGES
        from src.data_loader import load_all_data
        
        # Load data
        if 'data_dict' not in st.session_state:
            st.session_state.data_dict = load_all_data()

        if not st.session_state.data_dict or all(df.empty for df in st.session_state.data_dict.values() if hasattr(df, 'empty')):
            st.error("Application Initialization Failed: Could not load any datasets. Check paths and files.")
            st.stop()
        
        # Add the CSS styling
        st.markdown("""
        <style>
        /* Mobile responsive chart containers */
        .js-plotly-plot {
            margin-top: 10px !important;
            width: 100% !important;
        }
        
        /* Hide Plotly titles to prevent overlap with Streamlit */
        .js-plotly-plot .plotly .gtitle {
            display: none !important;
        }
        
        /* Responsive modebar positioning */
        .js-plotly-plot .plotly .modebar {
            top: 5px !important;
            right: 5px !important;
        }
        
        /* Modern Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #FAFAFA 0%, #F5F5F5 100%) !important;
            border-right: 2px solid #E0E0E0 !important;
        }
        
        /* Sidebar headers */
        .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
            color: #2c3e50 !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar widgets */
        .sidebar .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #E0E0E0 !important;
            border-radius: 0.75rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        .sidebar .stSlider > div > div {
            background-color: #FFFFFF !important;
            border-radius: 0.75rem !important;
            padding: 1rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Sidebar text */
        .sidebar .sidebar-content p, .sidebar .sidebar-content label {
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        /* Mobile breakpoints */
        @media (max-width: 768px) {
            .js-plotly-plot {
                height: auto !important;
                min-height: 300px !important;
            }
            
            .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
        }
        
        /* Tablet breakpoints */
        @media (max-width: 1024px) and (min-width: 769px) {
            .js-plotly-plot {
                min-height: 350px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.sidebar.header("Navigation")
        selection = st.sidebar.selectbox("Go To:", list(PAGES.keys()))

        page_func = PAGES[selection]
        page_func(st.session_state.data_dict)
        
        st.sidebar.markdown("---")
        st.sidebar.caption("Project: Pakistan Data Twin")
        
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

if __name__ == "__main__":
    main()