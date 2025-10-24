# src/app/main.py (dashboard revamp + deprecation-safe plotly usage)

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px 
from typing import Dict

# --- CRITICAL FIX FOR ModuleNotFoundError ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now imports from the 'src' package work correctly:
from src.data_loader import load_all_data
from src.config import DASHBOARD_INDICATORS, FORECASTING_INDICATORS, CATEGORY_MAPPING
# Import new multi-axis function along with existing ones
from src.charts import create_plot_type, get_kpi_value, create_multi_axis_plot


# Define a standard Plotly configuration for Streamlit (to address deprecation warning)
PLOTLY_CONFIG = {
    'displayModeBar': False,  # Hides the default Plotly menu
    'responsive': True,
    'scrollZoom': False  # Disable scroll-wheel zoom to prevent accidental zooming
}


# --- PAGE FUNCTION: Dashboard Overview ---

def render_dashboard(data_dict: Dict[str, pd.DataFrame]):
    """Beautiful, consistent dashboard layout (cards + trend + donuts)."""

    st.title("📊 Pakistan Data Twin Dashboard")
    st.caption("GDP, Education and Internet indicators with a clean, consistent layout.")
    st.markdown("---")

    # --- 1) Sidebar: Year range filter ---
    st.sidebar.subheader("Filters")
    all_years = []
    for df in data_dict.values():
        if not df.empty:
            all_years.extend(df['Year'].unique())
    if not all_years:
        st.warning("No data available to set filters. Check your data_processed folder.")
        return

    min_year, max_year = int(min(all_years)), int(max(all_years))
    selected_years = st.sidebar.slider(
        'Year range', min_value=min_year, max_value=max_year,
        value=(min_year, max_year), key="dashboard_year_filter"
    )

    # Filter all data upfront
    df_filtered: Dict[str, pd.DataFrame] = {}
    for cat, df in data_dict.items():
        if not df.empty:
            df_filtered[cat] = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

    # --- 2) KPI cards (top row) ---
    kpi_cols = st.columns(3)
    for i, category in enumerate(DASHBOARD_INDICATORS):
        df = df_filtered.get(category)
        if df is not None and not df.empty:
            value, delta = get_kpi_value(df, category)
            kpi_cols[i].metric(label=f"{category}", value=value, delta=f"{delta:.2f}% YoY")
        else:
            kpi_cols[i].metric(label=f"{category}", value="N/A", delta="N/A")

    st.markdown("---")

# --- 3) Main center: GDP ---
    left_spacer, center, right_spacer = st.columns([1, 2, 1])
    with center:
        df_gdp = df_filtered.get('GDP')
        if df_gdp is not None and not df_gdp.empty:
            fig_gdp = create_plot_type(df_gdp, 'GDP', 'area')
            fig_gdp.update_layout(height=460, title_font_size=18, margin=dict(t=40, l=0, r=0, b=20))
            st.plotly_chart(fig_gdp, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            st.error("GDP data not available.")

        # --- Beneath GDP: School Enrollment and Internet Usage histograms ---
        sub1, sub2 = st.columns(2)
        with sub1:
            df_edu = df_filtered.get('Education')
            if df_edu is not None and not df_edu.empty:
                fig_h1 = create_plot_type(df_edu, 'Education', 'hist')
                st.plotly_chart(fig_h1, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.warning("Education data not available.")
        with sub2:
            df_health = df_filtered.get('Health')
            if df_health is not None and not df_health.empty:
                fig_h2 = create_plot_type(df_health, 'Health', 'hist')
                st.plotly_chart(fig_h2, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.warning("Internet/Health data not available.")

    st.markdown("---")

    # --- 4) Last: Comparison chart (multi-axis) ---
    fig_multi = create_multi_axis_plot(df_filtered)
    st.plotly_chart(fig_multi, use_container_width=True, config=PLOTLY_CONFIG)

    st.caption("Left axis: GDP (USD, SI notation). Right axis: percentage scale 0–100%.")


# --- PAGE FUNCTION: Forecasting & Modeling (Remains Unchanged) ---

def render_forecasting(data_dict: Dict[str, pd.DataFrame]):
    """Renders the Forecasting & Modeling page (placeholder)."""

    st.title("🔮 Forecasting & Modeling")
    st.markdown("This section is where forecasting models for key indicators will be integrated.")

    st.sidebar.subheader("Forecasting Indicators")
    
    with st.sidebar.expander("Select Indicator", expanded=True):
        selected_category = st.radio(
            "Select Data Source:",
            FORECASTING_INDICATORS,
            index=0,
            key="forecasting_indicator_radio"
        )
    
    st.markdown(f"## {selected_category} Historical Data")
    st.markdown("---")
    
    df_current = data_dict.get(selected_category)
    if df_current is not None and not df_current.empty:
        st.info(f"The model will be trained on data from {df_current['Year'].min()} to {df_current['Year'].max()}")
        
        fig = create_plot_type(df_current, selected_category, 'line')
        # FIX: Using config dictionary
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        
        st.markdown("---")
        st.markdown("Future sections will include: Model Parameters, Forecast Chart, and Model Evaluation.")
    else:
        st.error(f"Data not available for {selected_category}.")


# --- MAIN ROUTER ---

PAGES = {
    "Dashboard Overview 📊": render_dashboard,
    "Forecasting & Modeling 🔮": render_forecasting,
}

def main():
    """Sets up the app structure and routes to the selected page."""

    st.set_page_config(
        page_title="Pakistan Data Twin Visualization",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'data_dict' not in st.session_state:
        st.session_state.data_dict = load_all_data()

    if not st.session_state.data_dict or all(df.empty for df in st.session_state.data_dict.values() if isinstance(df, pd.DataFrame)):
        st.error("Application Initialization Failed: Could not load any datasets. Check paths and files.")
        st.stop()
        
    st.sidebar.header("Navigation")
    selection = st.sidebar.selectbox("Go To:", list(PAGES.keys()))

    page_func = PAGES[selection]
    page_func(st.session_state.data_dict)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Project: Pakistan Data Twin")


if __name__ == "__main__":
    main()
