# src/app/main.py (FIXED DEPRECATION WARNINGS)

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
    'displayModeBar': False, # Hides the default Plotly menu (common request)
    'responsive': True,
    'scrollZoom': True # Allows zoom on the multi-axis plot
}


# --- PAGE FUNCTION: Dashboard Overview ---

def render_dashboard(data_dict: Dict[str, pd.DataFrame]):
    """Renders the Dashboard Overview page with the new visual layout."""

    st.title("📊 Key Socio-Economic Indicators Dashboard")
    st.markdown("A multi-view analysis of Pakistan's **GDP**, **Education**, and **Digital Penetration** trends with stylized visualizations.")
    st.markdown("---")

    # --- 1. SIDEBAR FILTER (Year Range) ---
    st.sidebar.subheader("Dashboard Filters")
    
    all_years = []
    for df in data_dict.values():
        if not df.empty:
            all_years.extend(df['Year'].unique())
            
    if not all_years:
        st.warning("No data available to set filters. Check your data_processed folder.")
        return

    min_year = int(min(all_years))
    max_year = int(max(all_years))
    
    selected_years = st.sidebar.slider(
        'Filter Year Range:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key="dashboard_year_filter" 
    )
    
    # Filter all data
    df_filtered = {}
    for cat, df in data_dict.items():
        if not df.empty:
            df_filtered[cat] = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]


    # --- 2. KPI Section (Row 1) ---
    st.subheader(f"Current Metrics Summary")
    kpi_cols = st.columns(3)
    
    for i, category in enumerate(DASHBOARD_INDICATORS):
        df = df_filtered.get(category)
        if df is not None and not df.empty:
            value, delta = get_kpi_value(df, category)
            kpi_cols[i].metric(
                label=f"Latest {category}",
                value=value,
                delta=f"{delta:.2f}% YoY"
            )
        else:
            kpi_cols[i].metric(label=f"Latest {category}", value="N/A", delta="N/A")
            
    st.markdown("---")


    # --- 3. Visualization Grid: Row 2 (3-Column Layout) ---
    # Layout: [Small Chart 1] | [BIG AREA CHART (GDP)] | [Small Chart 2]
    
    # Adjusted column ratio for aesthetic balance (1.2:2:1.2)
    col_small_1, col_big_center, col_small_2 = st.columns([1.2, 2, 1.2]) 

    # Chart 2.1 (Small Left): Education - Horizontal Bar Chart (STYLED HBAR)
    with col_small_1:
        df_edu_filtered = df_filtered.get('Education')
        if df_edu_filtered is not None and not df_edu_filtered.empty:
            fig = create_plot_type(df_edu_filtered, 'Education', 'hbar')
            # FIX: Using config dictionary
            st.plotly_chart(fig, width='stretch', config=PLOTLY_CONFIG)
        else:
            st.warning("Education Data not available.")

    # Chart 2.2 (BIG CENTER): GDP - Area Chart (STYLED AREA CHART)
    with col_big_center:
        df_gdp_filtered = df_filtered.get('GDP')
        if df_gdp_filtered is not None and not df_gdp_filtered.empty:
            fig = create_plot_type(df_gdp_filtered, 'GDP', 'area')
            # Set explicit height here to override the default and make it larger
            fig.update_layout(height=480, title_font_size=18, margin=dict(t=50, l=0, r=0, b=20)) 
            # FIX: Using config dictionary
            st.plotly_chart(fig, width='stretch', config=PLOTLY_CONFIG)
        else:
            st.error("GDP Data not available for Area Chart.")

    # Chart 2.3 (Small Right): Health/Digital Penetration - Pie Chart
    with col_small_2:
        df_net_filtered = df_filtered.get('Health')
        if df_net_filtered is not None and not df_net_filtered.empty:
            fig = create_plot_type(df_net_filtered, 'Health', 'pie')
            # FIX: Using config dictionary (Pie chart height is set in charts.py)
            st.plotly_chart(fig, width='stretch', config=PLOTLY_CONFIG)
        else:
            st.warning("Digital Penetration Data not available.")


    st.markdown("---")

    # --- 4. Visualization Grid: Row 3 (1-Column Layout + Text) ---
    col_chart_large, col_text = st.columns([3, 1])

    # Chart 3.1 (Large Chart): Combined Indicator Trend (MIXED SUBPLOTS)
    with col_chart_large:
        st.subheader("Combined Indicator Trend (Multi-Axis)")
        
        fig_multi = create_multi_axis_plot(data_dict)
        # FIX: Using config dictionary
        st.plotly_chart(fig_multi, width='stretch', config=PLOTLY_CONFIG)

    # Text 3.2 (Summary Text)
    with col_text:
        st.subheader("Insight Summary")
        st.info(
            f"The **GDP Area Chart** highlights the overall economic trajectory "
            f"from {selected_years[0]} to {selected_years[1]}. "
            f"The **Combined Trend Chart** uses a secondary Y-axis to correctly "
            f"compare the scale of GDP (left axis) against the percentage-based "
            f"indicators (right axis). This reveals potential correlations over time."
        )
        st.markdown("---")
        st.caption("The multi-axis chart is crucial for comparing metrics on vastly different scales.")


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
        st.plotly_chart(fig, width='stretch', config=PLOTLY_CONFIG)
        
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
