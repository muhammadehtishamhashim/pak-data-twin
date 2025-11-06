import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("⚡ Energy Dashboard")
    st.markdown("Explore Pakistan's Energy Sector - Track renewable energy adoption, power generation, and energy consumption patterns.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Capacity", "39,000 MW", "2,100 MW")
    
    with col2:
        st.metric("Renewable Share", "4.2%", "0.8%")
    
    with col3:
        st.metric("Per Capita", "500 kWh", "25 kWh")
    
    with col4:
        st.metric("Energy Mix", "Mixed", "Improving")
    
    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["⚡ Generation", "🌱 Renewables", "📊 Consumption"])
    
    with tab1:
        st.header("Power Generation")
        st.info("⚡ Power generation capacity and sources analysis")
        
        # Sample breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Thermal:** 64.2%")
            st.write("**Hydro:** 31.6%")
        
        with col2:
            st.write("**Nuclear:** 3.1%")
            st.write("**Renewables:** 1.1%")
    
    with tab2:
        st.header("Renewable Energy")
        st.info("🌱 Solar, wind, and other renewable energy sources")
        
        # Renewable breakdown
        st.write("**Solar Capacity:** 1,200 MW")
        st.write("**Wind Capacity:** 1,580 MW")
        st.write("**Biomass:** 200 MW")
    
    with tab3:
        st.header("Energy Consumption")
        st.info("📊 Energy consumption patterns and efficiency")
        
        # Consumption by sector
        st.write("**Industrial:** 27.4%")
        st.write("**Residential:** 46.8%")
        st.write("**Commercial:** 8.1%")
        st.write("**Agriculture:** 17.7%")
    
    st.markdown("---")
    st.markdown("*Energy sector analysis | Pakistan Data Twin Dashboard*")