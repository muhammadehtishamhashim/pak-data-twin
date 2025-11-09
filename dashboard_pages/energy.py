import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def load_energy_data():
    """Load and clean the renewable energy demand dataset"""
    try:
        df = pd.read_csv('datasets_raw/Energy/demandfordistributedrenewableenergygenerationinpakistan.csv')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert 2015 load data to numeric
        df['2015'] = pd.to_numeric(df['2015'], errors='coerce')
        
        # Clean consumer data columns
        df['Commercial: Load(KW)'] = pd.to_numeric(df['Commercial: Load(KW)'], errors='coerce')
        df['Industrial: Load(KW)'] = pd.to_numeric(df['Industrial: Load(KW)'], errors='coerce')
        df['T/Well Load(KW)'] = pd.to_numeric(df['T/Well Load(KW)'], errors='coerce')
        df['Total Load (KW)'] = pd.to_numeric(df['Total Load (KW)'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def show():
    st.title("⚡ Energy Dashboard")
    st.markdown("*Distributed Renewable Energy Generation Demand Analysis in Pakistan*")
    
    # Load data
    df = load_energy_data()
    
    if df is not None:
        # Calculate key metrics
        total_stations = df['Name of Grid Station'].nunique()
        total_feeders = len(df)
        avg_load_2015 = df['2015'].mean()
        total_capacity_kw = df['Total Load (KW)'].sum()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Grid Stations", f"{total_stations}", "132 KV")
        
        with col2:
            st.metric("Total Feeders", f"{total_feeders}", "Outgoing 11KV")
        
        with col3:
            st.metric("Avg Load 2015", f"{avg_load_2015:.0f} Amp", "Per Feeder")
        
        with col4:
            st.metric("Total Capacity", f"{total_capacity_kw/1000:.1f} MW", "Connected Load")
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["📊 Grid Analysis", "🏭 Consumer Distribution", "📈 Load Trends"])
        
        with tab1:
            st.subheader("Grid Station Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Load distribution by grid station
                station_load = df.groupby('Name of Grid Station')['Total Load (KW)'].sum().sort_values(ascending=False)
                
                fig_stations = px.bar(
                    x=station_load.index,
                    y=station_load.values,
                    title='Total Load by Grid Station',
                    labels={'x': 'Grid Station', 'y': 'Total Load (KW)'},
                    color=station_load.values,
                    color_continuous_scale='Greens'
                )
                fig_stations.update_layout(
                    showlegend=False,
                    xaxis_tickangle=-45,
                    height=400
                )
                fig_stations.update_traces(
                    hovertemplate="<b>%{x}</b><br>Total Load: %{y:,.0f} KW<extra></extra>"
                )
                st.plotly_chart(fig_stations, use_container_width=True)
            
            with col2:
                # Number of feeders per station
                feeders_per_station = df.groupby('Name of Grid Station').size().sort_values(ascending=False)
                
                fig_feeders = px.pie(
                    values=feeders_per_station.values,
                    names=feeders_per_station.index,
                    title='Distribution of Feeders by Grid Station',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Greens
                )
                fig_feeders.update_traces(
                    hovertemplate="<b>%{label}</b><br>Feeders: %{value}<br>Share: %{percent}<extra></extra>"
                )
                st.plotly_chart(fig_feeders, use_container_width=True)
            
            # Transformer capacity analysis
            st.subheader("Transformer Capacity Distribution")
            
            # Clean and convert capacity data
            df['Capacity_MVA'] = df['Power T/F capacity (MVA)'].str.extract('(\d+)').astype(float)
            capacity_dist = df.groupby('Capacity_MVA').size()
            
            fig_capacity = px.bar(
                x=capacity_dist.index,
                y=capacity_dist.values,
                title='Number of Transformers by Capacity (MVA)',
                labels={'x': 'Capacity (MVA)', 'y': 'Count'},
                color=capacity_dist.values,
                color_continuous_scale='Teal'
            )
            fig_capacity.update_layout(showlegend=False, height=350)
            fig_capacity.update_traces(
                hovertemplate="<b>Capacity:</b> %{x} MVA<br><b>Count:</b> %{y}<extra></extra>"
            )
            st.plotly_chart(fig_capacity, use_container_width=True)
        
        with tab2:
            st.subheader("Consumer Load Distribution")
            
            # Calculate total loads by consumer type
            commercial_load = df['Commercial: Load(KW)'].sum()
            industrial_load = df['Industrial: Load(KW)'].sum()
            tubewell_load = df['T/Well Load(KW)'].sum()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Consumer type distribution
                consumer_data = {
                    'Type': ['Commercial', 'Industrial', 'Tube Wells'],
                    'Load (KW)': [commercial_load, industrial_load, tubewell_load]
                }
                
                fig_consumer = px.pie(
                    consumer_data,
                    values='Load (KW)',
                    names='Type',
                    title='Load Distribution by Consumer Type',
                    hole=0.4,
                    color_discrete_sequence=['#0f4c3a', '#1a7f5f', '#4fd1a8']
                )
                fig_consumer.update_traces(
                    hovertemplate="<b>%{label}</b><br>Load: %{value:,.0f} KW<br>Share: %{percent}<extra></extra>"
                )
                st.plotly_chart(fig_consumer, use_container_width=True)
            
            with col2:
                # Top 10 feeders by total load
                top_feeders = df.nlargest(10, 'Total Load (KW)')[['Name of Outgoing 11Kv', 'Total Load (KW)', 'Name of Grid Station']]
                
                fig_top = px.bar(
                    top_feeders,
                    x='Name of Outgoing 11Kv',
                    y='Total Load (KW)',
                    title='Top 10 Feeders by Total Load',
                    color='Name of Grid Station',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_top.update_layout(
                    xaxis_tickangle=-45,
                    height=400
                )
                fig_top.update_traces(
                    hovertemplate="<b>%{x}</b><br>Load: %{y:,.0f} KW<br>Station: %{customdata[0]}<extra></extra>",
                    customdata=top_feeders[['Name of Grid Station']].values
                )
                st.plotly_chart(fig_top, use_container_width=True)
            
            # Consumer statistics
            st.subheader("Consumer Statistics Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Commercial Load", f"{commercial_load/1000:.1f} MW", f"{(commercial_load/(commercial_load+industrial_load+tubewell_load)*100):.1f}%")
            
            with col2:
                st.metric("Industrial Load", f"{industrial_load/1000:.1f} MW", f"{(industrial_load/(commercial_load+industrial_load+tubewell_load)*100):.1f}%")
            
            with col3:
                st.metric("Tube Well Load", f"{tubewell_load/1000:.1f} MW", f"{(tubewell_load/(commercial_load+industrial_load+tubewell_load)*100):.1f}%")
        
        with tab3:
            st.subheader("Load Trends (2011-2015)")
            
            # Prepare yearly load data
            yearly_data = []
            for year in ['2011', '2012', '2013', '2014', '2015']:
                try:
                    df[year] = pd.to_numeric(df[year], errors='coerce')
                    avg_load = df[year].mean()
                    if not np.isnan(avg_load):
                        yearly_data.append({'Year': int(year), 'Average Load (Amp)': avg_load})
                except:
                    pass
            
            if yearly_data:
                yearly_df = pd.DataFrame(yearly_data)
                
                fig_trend = px.line(
                    yearly_df,
                    x='Year',
                    y='Average Load (Amp)',
                    title='Average Load Trend (2011-2015)',
                    markers=True,
                    line_shape='spline'
                )
                fig_trend.update_traces(
                    line=dict(color='#0f4c3a', width=3),
                    marker=dict(size=10),
                    hovertemplate="<b>Year:</b> %{x}<br><b>Avg Load:</b> %{y:.1f} Amp<extra></extra>"
                )
                fig_trend.update_layout(height=400)
                st.plotly_chart(fig_trend, use_container_width=True)
            
            # Load distribution by grid station over time
            st.subheader("Grid Station Load Comparison (2015)")
            
            station_load_2015 = df.groupby('Name of Grid Station')['2015'].mean().sort_values(ascending=False)
            
            fig_station_trend = px.bar(
                x=station_load_2015.index,
                y=station_load_2015.values,
                title='Average Load by Grid Station (2015)',
                labels={'x': 'Grid Station', 'y': 'Average Load (Amp)'},
                color=station_load_2015.values,
                color_continuous_scale='Viridis'
            )
            fig_station_trend.update_layout(
                showlegend=False,
                xaxis_tickangle=-45,
                height=400
            )
            fig_station_trend.update_traces(
                hovertemplate="<b>%{x}</b><br>Avg Load: %{y:.1f} Amp<extra></extra>"
            )
            st.plotly_chart(fig_station_trend, use_container_width=True)
            
            # Loss analysis
            st.subheader("Technical & Administrative Losses (2013)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Technical losses
                df['Technical Losses'] = pd.to_numeric(df['%age Losses Technical (2013)'], errors='coerce')
                avg_tech_loss = df['Technical Losses'].mean()
                
                fig_tech = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=avg_tech_loss,
                    title={'text': "Average Technical Losses (%)"},
                    delta={'reference': 10},
                    gauge={
                        'axis': {'range': [None, 25]},
                        'bar': {'color': "#0f4c3a"},
                        'steps': [
                            {'range': [0, 10], 'color': "lightgreen"},
                            {'range': [10, 15], 'color': "yellow"},
                            {'range': [15, 25], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 15
                        }
                    }
                ))
                fig_tech.update_layout(height=300)
                st.plotly_chart(fig_tech, use_container_width=True)
            
            with col2:
                # Administrative losses
                df['Admin Losses'] = pd.to_numeric(df['%age Losses Administrative (2013)'], errors='coerce')
                avg_admin_loss = df['Admin Losses'].mean()
                
                fig_admin = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=avg_admin_loss,
                    title={'text': "Average Administrative Losses (%)"},
                    delta={'reference': 5},
                    gauge={
                        'axis': {'range': [None, 15]},
                        'bar': {'color': "#1a7f5f"},
                        'steps': [
                            {'range': [0, 5], 'color': "lightgreen"},
                            {'range': [5, 10], 'color': "yellow"},
                            {'range': [10, 15], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 10
                        }
                    }
                ))
                fig_admin.update_layout(height=300)
                st.plotly_chart(fig_admin, use_container_width=True)
    
    else:
        st.error("Unable to load energy data. Please check if the dataset is available.")
    
    st.markdown("---")
    st.markdown("*Energy sector analysis | Distributed Renewable Energy Generation Demand in Pakistan*")