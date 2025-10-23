# src/charts.py (FIXED VALUE ERROR: Must specify a fill 'value' or 'method')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
from typing import Dict, List
from src.config import CATEGORY_MAPPING, DASHBOARD_INDICATORS

# Define a custom color palette for styling consistency
COLOR_PRIMARY = '#1f77b4' # Plotly Blue
COLOR_ACCENT = '#ff7f0e'  # Plotly Orange
COLOR_GDP = '#1e88e5' # Strong Blue for Area
COLOR_EDU = '#4caf50' # Green for Education Bar

def get_kpi_value(df: pd.DataFrame, category: str) -> (str, float):
    """Calculates the latest available value for a KPI and its growth delta."""
    if df.empty:
        return "N/A", 0.0
    
    df_sorted = df.sort_values('Year', ascending=False)
    latest_value = df_sorted['Value'].iloc[0]
    
    delta = 0.0
    if len(df_sorted) >= 2:
        prev_value = df_sorted['Value'].iloc[1]
        if prev_value != 0:
            delta = ((latest_value - prev_value) / prev_value) * 100
    
    if category == 'GDP' or category == 'Energy':
        if latest_value >= 1e12:
            value_str = f"${latest_value / 1e12:,.2f} T"
        elif latest_value >= 1e9:
            value_str = f"${latest_value / 1e9:,.2f} B"
        else:
            value_str = f"${latest_value:,.0f}"
    else:
        value_str = f"{latest_value:,.2f}%"

    return value_str, delta

def create_plot_type(df_filtered: pd.DataFrame, category: str, chart_type: str):
    """Generates a Plotly Express chart based on the specified type with custom styling."""
    
    config = CATEGORY_MAPPING[category]
    y_label = config['y_axis']
    title_text = f'{config["indicator_name"].split(" (")[0]} ({category})'
    
    if df_filtered.empty:
        return px.scatter(title=f"{title_text}: No Data Available")

    # --- Chart Generation & Styling ---
    if chart_type == 'area': 
        # GDP Area Chart: Highly colored and stylized
        fig = px.area(
            df_filtered, 
            x='Year', 
            y='Value', 
            title=title_text, 
            labels={'Value': y_label, 'Year': 'Year'}, 
            template='plotly_white',
            color_discrete_sequence=[COLOR_GDP] # Use strong blue
        )
        fig.update_traces(
            line_width=2, 
            fill='tozeroy', 
            opacity=0.9,
            line=dict(color=COLOR_GDP, shape='spline'), # Smoother line
            marker=dict(size=6, color='white', line=dict(width=1, color=COLOR_GDP))
        )

    elif chart_type == 'hbar':
        # Education Horizontal Bar Chart: Colored, Stylized, attempting round look
        fig = px.bar(
            df_filtered,
            x='Value',
            y='Year',
            orientation='h',
            title=title_text,
            labels={'Value': y_label, 'Year': 'Year'},
            template='plotly_white',
            color_discrete_sequence=[COLOR_EDU] # Use green
        )
        # Styling for a clean, modern look (simulating soft corners using layout)
        fig.update_traces(
            marker_line_width=0, 
            opacity=0.9
        )
        fig.update_layout(
            yaxis={'categoryorder':'category ascending'},
            bargap=0.1, # Small gap between bars
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

    elif chart_type == 'pie':
        latest_year = df_filtered['Year'].max()
        latest_value = df_filtered[df_filtered['Year'] == latest_year]['Value'].iloc[0]
        
        pie_data = pd.DataFrame({
            'Metric': [f'{title_text} ({latest_year})', 'Remainder'],
            'Value': [latest_value, max(0, 100 - latest_value)]
        })
        
        fig = px.pie(
            pie_data, 
            names='Metric', 
            values='Value', 
            title=f'{title_text} Distribution ({latest_year})', 
            template='plotly_white',
            color_discrete_sequence=['#ff9800', '#cccccc'] # Orange/Grey palette
        )
        fig.update_layout(height=450, margin=dict(t=50, b=0, l=0, r=0))
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            marker=dict(line=dict(color='white', width=2)) # White border for separation
        )

    else:
        fig = px.line(df_filtered, x='Year', y='Value', title=title_text)

    # --- Layout Update ---
    fig.update_layout(
        title_font_size=14,
        xaxis_tickformat='d',
        margin=dict(t=30, l=0, r=0, b=20),
        height=350 
    )
    
    return fig


def create_multi_axis_plot(data_dict: Dict[str, pd.DataFrame]) -> go.Figure:
    """
    Creates a combined plot using make_subplots to compare GDP (left axis, bar) 
    and percentage indicators (right axis, line) due to scale difference.
    """
    
    # 1. Prepare Data
    df_gdp = data_dict.get('GDP')
    df_edu = data_dict.get('Education')
    df_health = data_dict.get('Health')

    if df_gdp.empty or df_edu.empty or df_health.empty:
        return go.Figure().update_layout(title="Multi-Axis Plot: Data Missing", height=500)

    # Filter to unique years 
    years = sorted(df_gdp['Year'].unique())
    
    # Standardize data for plotting (index by year)
    gdp_data = df_gdp.set_index('Year')['Value']
    edu_data = df_edu.set_index('Year')['Value']
    health_data = df_health.set_index('Year')['Value']

    # 2. Create Subplots object
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    gdp_label = CATEGORY_MAPPING['GDP']['y_axis']

    # 3. Add Traces (GDP on Primary Y-Axis)
    fig.add_trace(
        go.Bar(
            x=years, 
            y=gdp_data.reindex(years).fillna(0), # Fill missing GDP with 0 for bar chart
            name='GDP (USD)',
            marker_color=COLOR_ACCENT,
            opacity=0.7
        ),
        secondary_y=False,
    )

    # 4. Add Traces (Percentages on Secondary Y-Axis)
    # Education
    fig.add_trace(
        go.Scatter(
            x=years, 
            # FIX: Use float('nan') instead of None to correctly signal missing data to pandas/plotly
            y=edu_data.reindex(years).fillna(float('nan')),
            name='School Enrollment (%)',
            mode='lines+markers',
            line=dict(color=COLOR_EDU, width=3)
        ),
        secondary_y=True,
    )
    # Digital Penetration
    fig.add_trace(
        go.Scatter(
            x=years, 
            # FIX: Use float('nan') instead of None
            y=health_data.reindex(years).fillna(float('nan')),
            name='Digital Penetration (%)',
            mode='lines+markers',
            line=dict(color='#8e24aa', width=3, dash='dot') # Purple, dotted line
        ),
        secondary_y=True,
    )

    # 5. Update Layout and Axes
    fig.update_layout(
        title_text='<b>Comparison: GDP vs. Socio-Economic Indicators</b>',
        template='plotly_white',
        hovermode="x unified",
        margin=dict(t=50, b=20, l=40, r=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_xaxes(title_text="Year", type='category')

    # Primary Y-axis (Left) - GDP
    fig.update_yaxes(
        title_text=f"<b>GDP ({gdp_label})</b>", 
        secondary_y=False, 
        showgrid=False,
        tickformat='~s' # Uses SI notation (k, M, G, T) for large numbers
    )

    # Secondary Y-axis (Right) - Percentages
    fig.update_yaxes(
        title_text="<b>Percentage (%)</b>", 
        secondary_y=True,
        range=[0, 100], 
        tickformat='.0f'
    )
    
    fig.update_layout(height=500)

    return fig
