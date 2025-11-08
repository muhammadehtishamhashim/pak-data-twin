import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import datetime
import json
import plotly.io as pio

def show():
    # Custom CSS for better spacing
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    h1 {
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-size: 1.2rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📈 Economy Dashboard")
    st.markdown("*Comprehensive economic analysis of Pakistan's key indicators*")
    
    # Create tabs for Economic Data and Forecasts
    tab1, tab2 = st.tabs(["📊 Economic Data", "🔮 AI Forecasts"])
    
    with tab1:
        # Economic Data Dashboard
        # All economic visualizations in one tab
        
            # Key Metrics Row
        st.subheader("Key Economic Indicators")
        try:
            col1, col2, col3, col4 = st.columns(4)
        
            with col1:
                gdp_latest = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP.csv')['GDP (current US$)'].iloc[-1] / 1e9
                st.metric("GDP", f"${gdp_latest:.1f}B", "Current")
        
            with col2:
                exports_latest = pd.read_csv('datasets_cleaned/Economy/Export_of_Goods_&_Services.csv')['Value'].iloc[-1]
                st.metric("Exports", f"${exports_latest:.0f}M", "Latest")
        
            with col3:
                remit_latest = pd.read_csv('datasets_cleaned/Economy/Workers_Remittance.csv')['Value'].iloc[-1]
                st.metric("Remittances", f"${remit_latest:.0f}M", "Latest")
        
            with col4:
                investment_latest = pd.read_csv('datasets_cleaned/Economy/Total_Foreign_Investment.csv')['Value'].iloc[-1]
                st.metric("FDI", f"${investment_latest:.0f}M", "Latest")
        
        except Exception as e:
            st.error(f"Metrics calculation error: {e}")
    
        st.markdown("---")
    
        # GDP Analysis Section
        st.subheader("GDP Analysis")
        col1, col2 = st.columns([2, 1])
    
        with col1:
            try:
                # Load GDP data
                gdp_df = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP.csv', parse_dates=['Date'])
            
                # GDP Trend Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=gdp_df['Date'],
                    y=gdp_df['GDP (current US$)'] / 1e9,
                    mode='lines+markers',
                    name='GDP (Billions USD)',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=6),
                    hovertemplate="<b>Date:</b> %{x|%Y}<br>" +
                                  "<b>GDP:</b> $%{y:.1f} Billion USD<br>" +
                                  "<b>Original:</b> $%{customdata:,.0f} USD<br>" +
                                  "<b>Series:</b> Current US Dollars<br>" +
                                  "<extra></extra>",
                    customdata=gdp_df['GDP (current US$)']
                ))
            
                fig.update_layout(
                    title="Pakistan GDP Trend (1999-2025)<br><sub>Gross Domestic Product in current US dollars</sub>",
                    xaxis_title="Year",
                    yaxis_title="GDP (Billions USD)",
                    template="plotly_white",
                    height=400
                )
            
                st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"GDP data error: {e}")
    
        with col2:
            try:
                # GDP Growth Rate Chart using factors file
                gdp_factors_df = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP_2000-2025.csv', parse_dates=['Observation Date'])
            
                # Filter for growth rate data
                growth_data = gdp_factors_df[gdp_factors_df['Series name'] == 'Growth Rate of Real Gross Domestic Product'].copy()
                growth_data = growth_data.sort_values('Observation Date')
            
                fig_growth = go.Figure()
                fig_growth.add_trace(go.Bar(
                    x=growth_data['Observation Date'],
                    y=growth_data['Observation Value'],
                    name='GDP Growth Rate',
                    marker_color=['red' if x < 0 else 'green' for x in growth_data['Observation Value']],
                    hovertemplate="<b>Date:</b> %{x|%Y}<br>" +
                                  "<b>Growth Rate:</b> %{y:.2f}%<br>" +
                                  "<b>Status:</b> %{customdata}<br>" +
                                  "<b>Source:</b> Real GDP Growth<br>" +
                                  "<extra></extra>",
                    customdata=['Negative Growth' if x < 0 else 'Positive Growth' for x in growth_data['Observation Value']]
                ))
            
                fig_growth.update_layout(
                    title="Pakistan GDP Annual Growth Rate<br><sub>Real GDP growth rate from factors dataset</sub>",
                    yaxis_title="Growth Rate (%)",
                    xaxis_title="Year",
                    height=400,
                    template="plotly_white"
                )
            
                st.plotly_chart(fig_growth, use_container_width=True)
            
            except Exception as e:
                st.error(f"Growth calculation error: {e}")
    
        st.markdown("---")
    
        # GDP Composition Section
        st.subheader("GDP Sectoral Composition")
        try:
            # GDP Composition Pie Chart - Latest Year (Full Width)
            gdp_factors_df = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP_2000-2025.csv', parse_dates=['Observation Date'])
        
            # Get latest year data (2025)
            latest_data = gdp_factors_df[gdp_factors_df['Observation Date'] == gdp_factors_df['Observation Date'].max()]
        
            # Extract GDP components
            sectors = ['Commodity Producing Sector (a+b)', 'Agricultural Sector', 'Industrial Sector', 'Services Sector']
            sector_data = []
            sector_values = []
        
            for sector in sectors:
                sector_row = latest_data[latest_data['Series name'] == sector]
                if not sector_row.empty:
                    value = sector_row['Observation Value'].iloc[0]
                    # Clean up sector names for display
                    if 'Commodity Producing' in sector:
                        sector_data.append('Commodity Producing')
                    else:
                        sector_data.append(sector.replace(' Sector', ''))
                    sector_values.append(value)
        
            # Create modern pie chart with better sizing
            fig_pie = go.Figure(data=[go.Pie(
                labels=sector_data,
                values=sector_values,
                hole=0.4,  # Donut style for modern look
                textinfo='label+percent',
                textposition='outside',
                marker=dict(
                    colors=['#8B4513', '#2E8B57', '#FF6B35', '#4A90E2'],  # Modern color palette for 4 sectors
                    line=dict(color='#FFFFFF', width=3)
                ),
                hovertemplate="<b>%{label}</b><br>" +
                              "<b>Value:</b> Rs. %{value:,.0f} Million PKR<br>" +
                              "<b>Share:</b> %{percent}<br>" +
                              "<b>Year:</b> 2025<br>" +
                              "<extra></extra>",
                # Modern hover effects
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="gray",
                    font_size=14
                )
            )])
        
            fig_pie.update_traces(
                # Scale up effect on hover
                marker_line_width=2,
                opacity=0.9
            )
        
            fig_pie.update_layout(
                title="Pakistan GDP Sectoral Composition (2025)<br><sub>Breakdown of Gross Domestic Product by major economic sectors</sub>",
                height=500,  # Larger height for full-width display
                template="plotly_white",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                # Modern styling
                font=dict(size=12),
                margin=dict(t=100, b=100, l=50, r=50)
            )
        
            # Add animation and modern effects
            fig_pie.update_traces(
                textfont_size=12,
                pull=[0.08, 0.08, 0.08, 0.08]  # More separation for better visibility
            )
        
            st.plotly_chart(fig_pie, use_container_width=True)
        
        except Exception as e:
            st.error(f"GDP composition error: {e}")
    
        st.markdown("---")
    
        # Trade Analysis Section
        st.subheader("Trade & Exchange")
        col1, col2 = st.columns(2)
    
        with col1:
            try:
                # Exports Analysis
                exports_df = pd.read_csv('datasets_cleaned/Economy/Export_of_Goods_&_Services.csv', parse_dates=['Date'])
            
                fig_exports = px.area(
                    exports_df, 
                    x='Date', 
                    y='Value',
                    title='Pakistan Exports of Goods & Services<br><sub>Total export value over time</sub>',
                    color_discrete_sequence=['#ff7f0e']
                )
                fig_exports.update_layout(
                    yaxis_title="Export Value (Million USD)",
                    height=350,
                    template="plotly_white"
                )
                fig_exports.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Export Value:</b> $%{y:,.0f} Million USD<br>" +
                                  "<b>Series:</b> Total Goods & Services<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_exports, use_container_width=True)
            
                # Workers Remittances
                remit_df = pd.read_csv('datasets_cleaned/Economy/Workers_Remittance.csv', parse_dates=['Date'])
            
                fig_remit = px.line(
                    remit_df, 
                    x='Date', 
                    y='Value',
                    title='Workers Remittances to Pakistan<br><sub>Monthly remittances from overseas Pakistani workers</sub>',
                    color_discrete_sequence=['#2ca02c']
                )
                fig_remit.update_layout(
                    yaxis_title="Remittances (Million USD)",
                    height=350,
                    template="plotly_white"
                )
                fig_remit.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Remittances:</b> $%{y:,.2f} Million USD<br>" +
                                  "<b>Source:</b> Overseas Pakistani Workers<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_remit, use_container_width=True)
            
            except Exception as e:
                st.error(f"Trade data error: {e}")
    
        with col2:
            try:
                # Exchange Rates
                exchange_df = pd.read_csv('datasets_cleaned/Economy/Exchange_Rates.csv', parse_dates=['Date'])
            
                # Filter for main exchange rate indicators
                neer_data = exchange_df[exchange_df['Series_Name'].str.contains('Nominal Effective', na=False)]
                reer_data = exchange_df[exchange_df['Series_Name'].str.contains('Real Effective', na=False)]
            
                fig_exchange = go.Figure()
            
                if not neer_data.empty:
                    fig_exchange.add_trace(go.Scatter(
                        x=neer_data['Date'],
                        y=neer_data['Value'],
                        mode='lines',
                        name='NEER (Nominal)',
                        line=dict(color='blue', width=2),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>NEER Index:</b> %{y:.2f}<br>" +
                                      "<b>Base:</b> 2010 = 100<br>" +
                                      "<b>Type:</b> Nominal Effective Exchange Rate<br>" +
                                      "<extra></extra>"
                    ))
            
                if not reer_data.empty:
                    fig_exchange.add_trace(go.Scatter(
                        x=reer_data['Date'],
                        y=reer_data['Value'],
                        mode='lines',
                        name='REER (Real)',
                        line=dict(color='red', width=2),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>REER Index:</b> %{y:.2f}<br>" +
                                      "<b>Base:</b> 2010 = 100<br>" +
                                      "<b>Type:</b> Real Effective Exchange Rate<br>" +
                                      "<extra></extra>"
                    ))
            
                fig_exchange.update_layout(
                    title="Pakistan Exchange Rate Indices<br><sub>NEER vs REER (Base: 2010=100)</sub>",
                    yaxis_title="Index Value (Base: 2010=100)",
                    height=350,
                    template="plotly_white",
                    legend=dict(x=0.02, y=0.98)
                )
            
                st.plotly_chart(fig_exchange, use_container_width=True)
            
                # Import Payments - Convert to millions for better readability
                imports_df = pd.read_csv('datasets_cleaned/Economy/Pk_Imports_Payments.csv', parse_dates=['Date'])
                imports_df['Value_Million'] = imports_df['Value'] / 1000  # Convert to millions
            
                fig_imports = px.bar(
                    imports_df.tail(20), 
                    x='Date', 
                    y='Value_Million',
                    title='Import Payments: Freight & Insurance<br><sub>Recent 20 months of import-related payments</sub>',
                    color_discrete_sequence=['#d62728']
                )
                fig_imports.update_layout(
                    yaxis_title="Payment Value (Million USD)",
                    height=350,
                    template="plotly_white"
                )
                fig_imports.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Payment:</b> $%{y:,.2f} Million USD<br>" +
                                  "<b>Type:</b> Freight & Insurance<br>" +
                                  "<b>Category:</b> Import Payments<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_imports, use_container_width=True)
            
            except Exception as e:
                st.error(f"Exchange/Import data error: {e}")
    
        st.markdown("---")
    
        # Government Debt Analysis Section
        st.subheader("Government Debt Analysis")
        try:
            # Comprehensive Debt Analysis with Main Plot and Subplots
            debt_df = pd.read_csv('datasets_cleaned/Economy/Pakistan_Debt_and_Liabilities.csv', parse_dates=['Date'])
        
            # Filter for different debt categories
            total_debt_df = debt_df[debt_df['Series_Name'] == 'Total Debt and Liabilities (sum I to IX)'].copy()
            gross_public_df = debt_df[debt_df['Series_Name'] == 'Gross Public Debt (sum I to III)'].copy()
            domestic_debt_df = debt_df[debt_df['Series_Name'] == 'Government Domestic Debt'].copy()
            external_debt_df = debt_df[debt_df['Series_Name'] == 'Government External Debt'].copy()
            
            # Create subplots: 2 rows, 2 columns
            fig_debt = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Total Debt & Liabilities (Main)', 
                    'Gross Public Debt', 
                    'Government Domestic Debt', 
                    'Government External Debt'
                ),
                specs=[[{"colspan": 2}, None],
                       [{}, {}]],
                vertical_spacing=0.12,
                horizontal_spacing=0.1
            )
            
            # Main plot: Total Debt (spans full width)
            if not total_debt_df.empty:
                fig_debt.add_trace(
                    go.Scatter(
                        x=total_debt_df['Date'],
                        y=total_debt_df['Value'] / 1000,  # Convert to trillions
                        mode='lines+markers',
                        name='Total Debt & Liabilities',
                        line=dict(color='#e377c2', width=3),
                        marker=dict(size=4),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>Total Debt:</b> Rs. %{y:,.2f} Trillion PKR<br>" +
                                      "<b>Category:</b> All Government Debt (I-IX)<br>" +
                                      "<extra></extra>"
                    ),
                    row=1, col=1
                )
            
            # Subplot 1: Gross Public Debt
            if not gross_public_df.empty:
                fig_debt.add_trace(
                    go.Scatter(
                        x=gross_public_df['Date'],
                        y=gross_public_df['Value'] / 1000,  # Convert to trillions
                        mode='lines',
                        name='Gross Public Debt',
                        line=dict(color='#1f77b4', width=2),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>Gross Public Debt:</b> Rs. %{y:,.2f} Trillion PKR<br>" +
                                      "<b>Category:</b> Sum I to III<br>" +
                                      "<extra></extra>"
                    ),
                    row=2, col=1
                )
            
            # Subplot 2: Government Domestic Debt
            if not domestic_debt_df.empty:
                fig_debt.add_trace(
                    go.Scatter(
                        x=domestic_debt_df['Date'],
                        y=domestic_debt_df['Value'] / 1000,  # Convert to trillions
                        mode='lines',
                        name='Domestic Debt',
                        line=dict(color='#2ca02c', width=2),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>Domestic Debt:</b> Rs. %{y:,.2f} Trillion PKR<br>" +
                                      "<b>Category:</b> Government Domestic<br>" +
                                      "<extra></extra>"
                    ),
                    row=2, col=2
                )
            
            # Subplot 3: Government External Debt (overlaid on domestic for comparison)
            if not external_debt_df.empty:
                fig_debt.add_trace(
                    go.Scatter(
                        x=external_debt_df['Date'],
                        y=external_debt_df['Value'] / 1000,  # Convert to trillions
                        mode='lines',
                        name='External Debt',
                        line=dict(color='#ff7f0e', width=2),
                        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                      "<b>External Debt:</b> Rs. %{y:,.2f} Trillion PKR<br>" +
                                      "<b>Category:</b> Government External<br>" +
                                      "<extra></extra>"
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig_debt.update_layout(
                title="Pakistan Government Debt Analysis Dashboard<br><sub>Comprehensive breakdown of government debt categories</sub>",
                height=750,  # Increased height to accommodate bottom legend
                template="plotly_white",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,  # Position below the chart
                    xanchor="center",
                    x=0.5
                )
            )
            
            # Update y-axis titles
            fig_debt.update_yaxes(title_text="Debt Value (Trillion PKR)", row=1, col=1)
            fig_debt.update_yaxes(title_text="Debt Value (Trillion PKR)", row=2, col=1)
            fig_debt.update_yaxes(title_text="Debt Value (Trillion PKR)", row=2, col=2)
        
            # Update x-axis titles
            fig_debt.update_xaxes(title_text="Date", row=2, col=1)
            fig_debt.update_xaxes(title_text="Date", row=2, col=2)
        
            st.plotly_chart(fig_debt, use_container_width=True)
        
        except Exception as e:
            st.error(f"Debt data error: {e}")
    
        st.markdown("---")
    
        # Foreign Investment Analysis Section
        st.subheader("Foreign Investment Analysis")
        try:
            # Total Foreign Investment
            investment_df = pd.read_csv('datasets_cleaned/Economy/Total_Foreign_Investment.csv', parse_dates=['Date'])
        
            fig_investment = px.line(
                investment_df, 
                x='Date', 
                y='Value',
                title='Pakistan Total Foreign Investment<br><sub>Foreign Direct Investment and Portfolio Investment flows</sub>',
                color_discrete_sequence=['#9467bd']
            )
            fig_investment.update_layout(
                yaxis_title="Investment Value (Million USD)",
                height=500,
                template="plotly_white"
            )
            fig_investment.update_traces(
                hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                              "<b>Investment:</b> $%{y:,.2f} Million USD<br>" +
                              "<b>Type:</b> Total Foreign Investment<br>" +
                              "<b>Includes:</b> FDI + Portfolio Investment<br>" +
                              "<extra></extra>"
            )
        
            st.plotly_chart(fig_investment, use_container_width=True)
        
        except Exception as e:
            st.error(f"Investment data error: {e}")
    
        st.markdown("---")
    
        # Net Balance PKR Exports Section
        st.subheader("Net Export Balance Analysis")
        try:
            # Net Balance PKR Exports
            net_balance_df = pd.read_csv('datasets_cleaned/Economy/Net-balance-PKR-Exports.csv', parse_dates=['Date'])
        
            fig_net_balance = px.bar(
                net_balance_df, 
                x='Date', 
                y='Value',
                title='Pakistan Net Export Balance<br><sub>Net export of goods (merchant) in PKR</sub>',
                color_discrete_sequence=['#17becf']
            )
            fig_net_balance.update_layout(
                yaxis_title="Net Export Balance (Million PKR)",
                xaxis_title="Year",
                height=500,
                template="plotly_white"
            )
            fig_net_balance.update_traces(
                hovertemplate="<b>Date:</b> %{x|%Y}<br>" +
                              "<b>Net Balance:</b> Rs. %{y:,.0f} Million PKR<br>" +
                              "<b>Type:</b> Net Export Goods (Merchant)<br>" +
                              "<b>Currency:</b> Pakistani Rupee<br>" +
                              "<extra></extra>"
            )
        
            st.plotly_chart(fig_net_balance, use_container_width=True)
        
        except Exception as e:
            st.error(f"Net balance data error: {e}")
    
        st.markdown("---")
    
        # Sectoral Analysis Section
        st.subheader("Sectoral Analysis")
        col1, col2 = st.columns(2)
    
        with col1:
            try:
                # Agriculture Sector
                agri_df = pd.read_csv('datasets_cleaned/Economy/Agriculture-Sector.csv', parse_dates=['Date'])
            
                fig_agri = px.line(
                    agri_df, 
                    x='Date', 
                    y='Value',
                    title='Agriculture Sector Growth Rate<br><sub>Quarterly growth performance in agriculture sector</sub>',
                    color_discrete_sequence=['#8c564b']
                )
                fig_agri.update_layout(
                    yaxis_title="Growth Rate (%)",
                    height=350,
                    template="plotly_white"
                )
                fig_agri.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Growth Rate:</b> %{y:.2f}%<br>" +
                                  "<b>Sector:</b> Agriculture<br>" +
                                  "<b>Frequency:</b> Quarterly<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_agri, use_container_width=True)
            
                # Services Export
                services_df = pd.read_csv('datasets_cleaned/Economy/Services-Export.csv', parse_dates=['Date'])
            
                fig_services = px.bar(
                    services_df.tail(15), 
                    x='Date', 
                    y='Value',
                    title='Pakistan Services Export (Recent 15 Months)<br><sub>Monthly export value of services sector</sub>',
                    color_discrete_sequence=['#17becf']
                )
                fig_services.update_layout(
                    yaxis_title="Export Value (Million USD)",
                    height=350,
                    template="plotly_white"
                )
                fig_services.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Export Value:</b> $%{y:,.0f} Million USD<br>" +
                                  "<b>Category:</b> Services Export<br>" +
                                  "<b>Period:</b> Monthly Data<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_services, use_container_width=True)
            
            except Exception as e:
                st.error(f"Sectoral data error: {e}")
    
        with col2:
            try:
                # CPI (Inflation) - Fixed column name
                cpi_df = pd.read_csv('datasets_cleaned/Economy/Pakistan-CPI_Annual.csv', parse_dates=['Date'])
            
                fig_cpi = px.line(
                    cpi_df, 
                    x='Date', 
                    y='CPI_Value',  # Fixed: using correct column name
                    title='Consumer Price Index - Annual<br><sub>Inflation indicator based on consumer prices</sub>',
                    color_discrete_sequence=['#ff7f0e']
                )
                fig_cpi.update_layout(
                    yaxis_title="CPI Index Value",
                    height=350,
                    template="plotly_white"
                )
                fig_cpi.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>CPI Value:</b> %{y:.2f}<br>" +
                                  "<b>Indicator:</b> Consumer Price Index<br>" +
                                  "<b>Frequency:</b> Annual Data<br>" +
                                  "<extra></extra>"
                )
            
                st.plotly_chart(fig_cpi, use_container_width=True)
            
                # Export by Commodities (sample) - Convert to millions for better readability
                commodities_df = pd.read_csv('datasets_cleaned/Economy/Export_By_Commodities.csv', parse_dates=['Date'])
                commodities_df['Value_Million'] = commodities_df['Value'] / 1000  # Convert from thousands to millions
            
                fig_commodities = px.area(
                    commodities_df.tail(50), 
                    x='Date', 
                    y='Value_Million',
                    title='Export by Commodities Trend (Recent 50 Records)<br><sub>Other exports category - monthly commodity export values</sub>',
                    color_discrete_sequence=['#bcbd22']
                )
                fig_commodities.update_layout(
                    yaxis_title="Export Value (Million USD)",
                    height=350,
                    template="plotly_white"
                )
                fig_commodities.update_traces(
                    hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                                  "<b>Export Value:</b> $%{y:.2f} Million USD<br>" +
                                  "<b>Original:</b> $%{customdata:,.0f} Thousand USD<br>" +
                                  "<b>Category:</b> Other Exports<br>" +
                                  "<extra></extra>",
                    customdata=commodities_df.tail(50)['Value'],
                    fill='tonexty'
                )
            
                st.plotly_chart(fig_commodities, use_container_width=True)
            
            except Exception as e:
                st.error(f"CPI/Commodities data error: {e}")
    
        st.markdown("---")
    
        # Combined Overview Dashboard
        st.subheader("Economic Overview Dashboard")
        try:
            # Create a multi-indicator dashboard
            fig_overview = make_subplots(
                rows=2, cols=2,
                subplot_titles=('GDP Trend', 'Trade Balance', 'Investment Flow', 'Inflation'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
        
            # GDP
            gdp_data = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP.csv', parse_dates=['Date'])
            fig_overview.add_trace(
                go.Scatter(x=gdp_data['Date'], y=gdp_data['GDP (current US$)']/1e9, 
                          name='GDP', line=dict(color='blue'),
                          hovertemplate="<b>GDP:</b> $%{y:.1f}B USD<br><b>Date:</b> %{x|%Y}<extra></extra>"),
                row=1, col=1
            )
        
            # Exports
            exports_data = pd.read_csv('datasets_cleaned/Economy/Export_of_Goods_&_Services.csv', parse_dates=['Date'])
            fig_overview.add_trace(
                go.Scatter(x=exports_data['Date'], y=exports_data['Value'], 
                          name='Exports', line=dict(color='green'),
                          hovertemplate="<b>Exports:</b> $%{y:,.0f}M USD<br><b>Date:</b> %{x|%B %Y}<extra></extra>"),
                row=1, col=2
            )
        
            # Investment
            investment_data = pd.read_csv('datasets_cleaned/Economy/Total_Foreign_Investment.csv', parse_dates=['Date'])
            fig_overview.add_trace(
                go.Scatter(x=investment_data['Date'], y=investment_data['Value'], 
                          name='Investment', line=dict(color='purple'),
                          hovertemplate="<b>Investment:</b> $%{y:,.2f}M USD<br><b>Date:</b> %{x|%B %Y}<extra></extra>"),
                row=2, col=1
            )
        
            # CPI - Fixed column name
            cpi_data = pd.read_csv('datasets_cleaned/Economy/Pakistan-CPI_Annual.csv', parse_dates=['Date'])
            fig_overview.add_trace(
                go.Scatter(x=cpi_data['Date'], y=cpi_data['CPI_Value'],  # Fixed: using correct column name
                          name='CPI', line=dict(color='orange'),
                          hovertemplate="<b>CPI:</b> %{y:.2f}<br><b>Date:</b> %{x|%Y}<extra></extra>"),
                row=2, col=2
            )
        
            fig_overview.update_layout(
                height=600,
                showlegend=False,
                template="plotly_white",
                title_text="Pakistan Economic Overview Dashboard"
            )
        
            st.plotly_chart(fig_overview, use_container_width=True)
        
        except Exception as e:
            st.error(f"Overview dashboard error: {e}")
    
    with tab2:
        # AI Forecasts Tab - Load pre-generated forecast plots
        st.subheader("🔮 AI-Powered Economic Forecasts")
        st.markdown("*Pre-generated LSTM model predictions for key economic indicators*")
        
        # Define the forecast files
        forecast_files = {
            'GDP LSTM Forecast': 'saved_plots/gdp_lstm_forecast_plot.json',
            'Debt Forecast': 'saved_plots/debt_forecast_plot.json',
            'Service Exports Forecast': 'saved_plots/service_exports_forecast_plot.json',
            'Commodities Export Forecast': 'saved_plots/commodities_export.json'
        }
        
        # Load and display each forecast
        for title, filepath in forecast_files.items():
            try:
                st.markdown(f"### 📈 {title}")
                
                # Check if file exists
                if os.path.exists(filepath):
                    # Read the JSON file
                    with open(filepath, 'r') as f:
                        fig_json = json.load(f)
                    
                    # Create Plotly figure from JSON
                    fig = pio.from_json(json.dumps(fig_json))
                    
                    # Display the figure
                    st.plotly_chart(fig, use_container_width=True)
                    st.success(f"✅ {title} loaded successfully")
                else:
                    st.warning(f"⚠️ Forecast file not found: {filepath}")
                    st.info(f"Please ensure the forecast model has been run and the plot saved to: `{filepath}`")
                
                st.markdown("---")
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Error decoding JSON for {title}: {e}")
                st.info("The JSON file may be corrupted or improperly formatted.")
            except Exception as e:
                st.error(f"❌ Error loading {title}: {e}")
                st.info(f"Please check if the file exists at: `{filepath}`")
        
        # Forecast Information
        with st.expander("ℹ️ About These Forecasts"):
            st.markdown("""
            **Forecast Models:**
            
            These forecasts are generated using LSTM (Long Short-Term Memory) neural networks trained on historical economic data.
            
            **Available Forecasts:**
            1. **GDP LSTM Forecast**: 10-year GDP projections based on historical trends
            2. **Debt Forecast**: Government debt trajectory predictions
            3. **Service Exports Forecast**: Service sector export predictions
            4. **Commodities Export Forecast**: Commodity export forecasts
            
            **Model Information:**
            - **Architecture**: Multi-layer LSTM networks
            - **Training Data**: Historical economic indicators from 1999-2025
            - **Validation**: Cross-validated on held-out test sets
            - **Update Frequency**: Models are retrained periodically with new data
            
            **Limitations:**
            - Forecasts assume continuation of historical patterns
            - Cannot predict unprecedented events or structural changes
            - Accuracy decreases with longer forecast horizons
            - Should be used as guidance, not absolute predictions
            
            **Note**: If forecasts are not displaying, please run the respective Jupyter notebooks in the `notebooks/` directory to generate the forecast plots.
            """)
    
    # Footer
    st.markdown("---")
    st.caption("*Pakistan Economic Data Analysis | Real-time economic indicators & AI forecasts*")