import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def load_immunization_data():
    """Load and clean the immunization coverage dataset"""
    try:
        df = pd.read_csv('datasets_raw/Health/immunization-coverage-in-thousands-pakistan-in-last-ten-years.csv')
        
        # Clean numeric columns (remove commas and convert to float)
        for col in df.columns[1:]:
            df[col] = df[col].replace('-', np.nan)
            df[col] = df[col].str.replace(',', '').astype(float)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def show():
    st.title("🏥 Health Dashboard")
    st.markdown("*Immunization Coverage Analysis in Pakistan (2011-2020)*")
    
    # Load data
    df = load_immunization_data()
    
    if df is not None:
        # Calculate key metrics
        latest_year = df['Year'].max()
        latest_data = df[df['Year'] == latest_year].iloc[0]
        
        total_doses_2020 = latest_data[1:].sum()
        total_doses_all = df.iloc[:, 1:].sum().sum()
        
        # Calculate growth rates
        first_year_total = df[df['Year'] == df['Year'].min()].iloc[0, 1:].sum()
        growth_rate = ((total_doses_2020 - first_year_total) / first_year_total) * 100
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Doses (2020)", f"{total_doses_2020/1000:.1f}M", f"+{growth_rate:.1f}%")
        
        with col2:
            polio_2020 = latest_data['Polio']
            st.metric("Polio Doses (2020)", f"{polio_2020/1000:.1f}M", "Highest")
        
        with col3:
            measles_2020 = latest_data['Measles']
            st.metric("Measles (2020)", f"{measles_2020/1000:.1f}M", "Coverage")
        
        with col4:
            st.metric("Years Tracked", "10", "2011-2020")
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["📈 Trends Over Time", "💉 Vaccine Comparison", "📊 Coverage Analysis"])
        
        with tab1:
            st.subheader("Immunization Trends (2011-2020)")
            
            # Line chart for all vaccines over time
            fig_trends = go.Figure()
            
            vaccines = df.columns[1:].tolist()
            colors = ['#0f4c3a', '#1a7f5f', '#2ea87e', '#4fd1a8', '#7ee5c7', '#a8e6cf']
            
            for i, vaccine in enumerate(vaccines):
                fig_trends.add_trace(go.Scatter(
                    x=df['Year'],
                    y=df[vaccine],
                    mode='lines+markers',
                    name=vaccine,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8),
                    hovertemplate=f"<b>{vaccine}</b><br>Year: %{{x}}<br>Doses: %{{y:,.0f}} thousand<extra></extra>"
                ))
            
            fig_trends.update_layout(
                title='Immunization Coverage Trends by Vaccine Type',
                xaxis_title='Year',
                yaxis_title='Doses Administered (Thousands)',
                height=500,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
            
            # Growth rate analysis
            st.subheader("Year-over-Year Growth Rates")
            
            growth_data = []
            for vaccine in vaccines:
                first_val = df[df['Year'] == df['Year'].min()][vaccine].values[0]
                last_val = df[df['Year'] == df['Year'].max()][vaccine].values[0]
                if not np.isnan(first_val) and not np.isnan(last_val):
                    growth = ((last_val - first_val) / first_val) * 100
                    growth_data.append({'Vaccine': vaccine, 'Growth (%)': growth})
            
            growth_df = pd.DataFrame(growth_data)
            
            fig_growth = px.bar(
                growth_df,
                x='Vaccine',
                y='Growth (%)',
                title='Overall Growth Rate (2011-2020)',
                color='Growth (%)',
                color_continuous_scale='RdYlGn',
                text='Growth (%)'
            )
            fig_growth.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>"
            )
            fig_growth.update_layout(
                showlegend=False,
                xaxis_tickangle=-45,
                height=400
            )
            
            st.plotly_chart(fig_growth, use_container_width=True)
        
        with tab2:
            st.subheader("Vaccine Distribution Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart for 2020 distribution
                latest_vaccines = latest_data[1:].dropna()
                
                fig_pie = px.pie(
                    values=latest_vaccines.values,
                    names=latest_vaccines.index,
                    title=f'Vaccine Distribution in {latest_year}',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Greens
                )
                fig_pie.update_traces(
                    hovertemplate="<b>%{label}</b><br>Doses: %{value:,.0f} thousand<br>Share: %{percent}<extra></extra>"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Total doses by vaccine (2011-2020)
                total_by_vaccine = df.iloc[:, 1:].sum().sort_values(ascending=False)
                
                fig_total = px.bar(
                    x=total_by_vaccine.index,
                    y=total_by_vaccine.values,
                    title='Total Doses Administered (2011-2020)',
                    labels={'x': 'Vaccine', 'y': 'Total Doses (Thousands)'},
                    color=total_by_vaccine.values,
                    color_continuous_scale='Teal'
                )
                fig_total.update_layout(
                    showlegend=False,
                    xaxis_tickangle=-45,
                    height=400
                )
                fig_total.update_traces(
                    hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f} thousand doses<extra></extra>"
                )
                st.plotly_chart(fig_total, use_container_width=True)
            
            # Heatmap of vaccination coverage
            st.subheader("Vaccination Coverage Heatmap")
            
            # Prepare data for heatmap
            heatmap_data = df.set_index('Year').T
            
            fig_heatmap = px.imshow(
                heatmap_data,
                labels=dict(x="Year", y="Vaccine", color="Doses (Thousands)"),
                title="Immunization Coverage Intensity (2011-2020)",
                color_continuous_scale='Greens',
                aspect="auto"
            )
            fig_heatmap.update_traces(
                hovertemplate="<b>%{y}</b><br>Year: %{x}<br>Doses: %{z:,.0f} thousand<extra></extra>"
            )
            fig_heatmap.update_layout(height=400)
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab3:
            st.subheader("Detailed Coverage Analysis")
            
            # Individual vaccine trends
            st.markdown("#### Select Vaccine for Detailed Analysis")
            
            selected_vaccine = st.selectbox(
                "Choose a vaccine:",
                vaccines,
                index=1  # Default to Polio
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Line chart for selected vaccine
                fig_selected = px.line(
                    df,
                    x='Year',
                    y=selected_vaccine,
                    title=f'{selected_vaccine} Coverage Trend',
                    markers=True
                )
                fig_selected.update_traces(
                    line=dict(color='#0f4c3a', width=4),
                    marker=dict(size=10),
                    hovertemplate="<b>Year:</b> %{x}<br><b>Doses:</b> %{y:,.0f} thousand<extra></extra>"
                )
                fig_selected.update_layout(
                    yaxis_title='Doses (Thousands)',
                    height=350
                )
                st.plotly_chart(fig_selected, use_container_width=True)
            
            with col2:
                # Statistics for selected vaccine
                vaccine_data = df[selected_vaccine].dropna()
                
                st.markdown(f"**{selected_vaccine} Statistics:**")
                st.write(f"• **Average (2011-2020):** {vaccine_data.mean():,.0f} thousand doses")
                st.write(f"• **Highest:** {vaccine_data.max():,.0f} thousand ({df[df[selected_vaccine] == vaccine_data.max()]['Year'].values[0]})")
                st.write(f"• **Lowest:** {vaccine_data.min():,.0f} thousand ({df[df[selected_vaccine] == vaccine_data.min()]['Year'].values[0]})")
                st.write(f"• **Total (10 years):** {vaccine_data.sum():,.0f} thousand doses")
                st.write(f"• **Std Deviation:** {vaccine_data.std():,.0f} thousand")
                
                # Gauge chart for latest year
                latest_val = latest_data[selected_vaccine]
                max_val = vaccine_data.max()
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=latest_val,
                    title={'text': f"{selected_vaccine} - {latest_year}"},
                    delta={'reference': vaccine_data.mean()},
                    gauge={
                        'axis': {'range': [None, max_val * 1.2]},
                        'bar': {'color': "#0f4c3a"},
                        'steps': [
                            {'range': [0, vaccine_data.mean()], 'color': "lightgray"},
                            {'range': [vaccine_data.mean(), max_val], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': max_val
                        }
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Comparative analysis table
            st.subheader("Yearly Comparison Table")
            
            # Format the dataframe for display
            display_df = df.copy()
            for col in display_df.columns[1:]:
                display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}" if not pd.isna(x) else "N/A")
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Summary statistics
            st.subheader("Summary Statistics (All Vaccines)")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Doses (10 years)", f"{total_doses_all/1000:.1f}M", "All Vaccines")
            
            with col2:
                avg_annual = total_doses_all / 10
                st.metric("Average Annual Doses", f"{avg_annual/1000:.1f}M", "Per Year")
            
            with col3:
                most_administered = df.iloc[:, 1:].sum().idxmax()
                st.metric("Most Administered", most_administered, f"{df[most_administered].sum()/1000:.1f}M")
    
    else:
        st.error("Unable to load immunization data. Please check if the dataset is available.")
    
    st.markdown("---")
    st.markdown("*Health sector analysis | Immunization Coverage in Pakistan (2011-2020)*")