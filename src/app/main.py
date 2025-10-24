# src/app/main.py (dashboard revamp + deprecation-safe plotly usage)

import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
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
    'displayModeBar': True,  # Show modebar for better interactivity
    'displaylogo': False,    # Hide Plotly logo
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],  # Remove unnecessary buttons
    'responsive': True,      # Make charts responsive
    'scrollZoom': False,     # Disable scroll-wheel zoom to prevent accidental zooming
    'doubleClick': 'reset'   # Double-click to reset zoom
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

# --- 3) Enhanced GDP Chart (Full Width, Bigger, More Stylized) ---
    st.subheader("📈 Pakistan GDP Growth Trajectory")
    df_gdp = df_filtered.get('GDP')
    if df_gdp is not None and not df_gdp.empty:
        # Create enhanced GDP area chart with better styling
        fig_gdp = px.area(
            df_gdp, 
            x='Year', 
            y='Value',
            title='Pakistan GDP (Current US$) - Economic Growth Over Time',
            labels={'Value': 'GDP (USD)', 'Year': 'Year'},
            template='plotly_white'
        )
        
        # Enhanced styling for GDP chart
        fig_gdp.update_traces(
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.3)',
            line=dict(color='#1f77b4', width=4, shape='spline'),
            marker=dict(size=8, color='white', line=dict(width=2, color='#1f77b4')),
            hovertemplate='<b>GDP</b><br>Year: %{x}<br>Value: $%{y:,.0f}<extra></extra>'
        )
        
        fig_gdp.update_layout(
            height=600,  # Bigger height
            title=dict(
                text='<b>Pakistan GDP (Current US$) - Economic Growth Over Time</b>',
                x=0.5,
                font=dict(size=24, color='#2c3e50')
            ),
            xaxis=dict(
                title=dict(text='Year', font=dict(size=16)),
                tickfont=dict(size=14),
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                title=dict(text='GDP (USD)', font=dict(size=16)),
                tickfont=dict(size=14),
                tickformat='$,.0s',
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=80, l=80, r=80, b=80),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_gdp, use_container_width=True, config=PLOTLY_CONFIG)
    else:
        st.error("GDP data not available.")

    st.markdown("---")

    # --- 4) Enhanced Side-by-Side Charts (Education & Internet Usage) ---
    st.subheader("📊 Social Development Indicators Distribution")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        df_edu = df_filtered.get('Education')
        if df_edu is not None and not df_edu.empty:
            # Enhanced Education histogram
            fig_edu = px.histogram(
                df_edu, 
                x='Value',
                nbins=15,
                title='School Enrollment Distribution (%)',
                labels={'Value': 'Enrollment Rate (%)', 'count': 'Frequency'},
                template='plotly_white'
            )
            
            fig_edu.update_traces(
                marker=dict(color='#2ca02c', opacity=0.8, line=dict(color='white', width=1)),
                hovertemplate='<b>School Enrollment</b><br>Range: %{x:.1f}%<br>Count: %{y}<extra></extra>'
            )
            
            fig_edu.update_layout(
                height=450,
                title=dict(
                    text='<b>School Enrollment Distribution</b>',
                    x=0.5,
                    font=dict(size=18, color='#2c3e50')
                ),
                xaxis=dict(
                    title=dict(text='Enrollment Rate (%)', font=dict(size=14)),
                    tickfont=dict(size=12),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                yaxis=dict(
                    title=dict(text='Frequency', font=dict(size=14)),
                    tickfont=dict(size=12),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=60, l=60, r=60, b=60),
                bargap=0.1
            )
            
            st.plotly_chart(fig_edu, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            st.warning("Education data not available.")
    
    with col2:
        df_health = df_filtered.get('Health')
        if df_health is not None and not df_health.empty:
            # Enhanced Internet Usage histogram
            fig_health = px.histogram(
                df_health, 
                x='Value',
                nbins=15,
                title='Internet Usage Distribution (%)',
                labels={'Value': 'Internet Users (%)', 'count': 'Frequency'},
                template='plotly_white'
            )
            
            fig_health.update_traces(
                marker=dict(color='#ff7f0e', opacity=0.8, line=dict(color='white', width=1)),
                hovertemplate='<b>Internet Usage</b><br>Range: %{x:.1f}%<br>Count: %{y}<extra></extra>'
            )
            
            fig_health.update_layout(
                height=450,
                title=dict(
                    text='<b>Internet Usage Distribution</b>',
                    x=0.5,
                    font=dict(size=18, color='#2c3e50')
                ),
                xaxis=dict(
                    title=dict(text='Internet Users (%)', font=dict(size=14)),
                    tickfont=dict(size=12),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                yaxis=dict(
                    title=dict(text='Frequency', font=dict(size=14)),
                    tickfont=dict(size=12),
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=60, l=60, r=60, b=60),
                bargap=0.1
            )
            
            st.plotly_chart(fig_health, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            st.warning("Internet usage data not available.")

    st.markdown("---")

    st.markdown("---")
    
    # --- 5) Enhanced Multi-Axis Comparison Chart ---
    st.subheader("🔄 Comprehensive Development Indicators Comparison")
    
    # Create enhanced multi-axis chart with better styling
    fig_multi = create_multi_axis_plot(df_filtered)
    
    # Apply additional styling to the multi-axis chart
    fig_multi.update_layout(
        height=550,
        title=dict(
            text='<b>Pakistan Development Indicators: GDP vs Social Metrics</b>',
            x=0.5,
            font=dict(size=22, color='#2c3e50')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, l=80, r=80, b=80),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_multi, use_container_width=True, config=PLOTLY_CONFIG)

    # Enhanced caption with better formatting
    st.info("📊 **Chart Guide:** Blue bars represent GDP in USD (left axis), while colored lines show percentage indicators (right axis). This visualization helps identify correlations between economic growth and social development.")
    
    # Add some spacing at the bottom
    st.markdown("<br>", unsafe_allow_html=True)


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
        page_title="Pakistan Data Twin Dashboard",
        page_icon="📊",
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
