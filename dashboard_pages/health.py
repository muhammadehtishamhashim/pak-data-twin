import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("🏥 Health Dashboard")
    st.markdown("Monitor Pakistan's Health Indicators - Examine healthcare statistics, immunization coverage, and public health trends.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Life Expectancy", "67.3 years", "1.2 years")
    
    with col2:
        st.metric("Infant Mortality", "57 per 1000", "-3 per 1000")
    
    with col3:
        st.metric("Vaccination Rate", "78%", "5%")
    
    with col4:
        st.metric("Doctors per 1000", "1.0", "0.1")
    
    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["🏥 Healthcare", "💉 Immunization", "📊 Statistics"])
    
    with tab1:
        st.header("Healthcare System")
        st.info("🏥 Healthcare infrastructure and services analysis")
        
        # Healthcare facilities
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Hospitals:** 1,279")
            st.write("**Basic Health Units:** 5,527")
        
        with col2:
            st.write("**Doctors:** 240,000+")
            st.write("**Nurses:** 110,000+")
    
    with tab2:
        st.header("Immunization Coverage")
        st.info("💉 Vaccination programs and coverage rates")
        
        # Vaccination rates
        st.write("**DPT3 Coverage:** 75%")
        st.write("**Measles Coverage:** 71%")
        st.write("**Polio Eradication:** Ongoing")
    
    with tab3:
        st.header("Health Statistics")
        st.info("📊 Key health indicators and trends")
        
        # Health indicators
        st.write("**Maternal Mortality:** 140 per 100,000")
        st.write("**Under-5 Mortality:** 69 per 1,000")
        st.write("**Malnutrition Rate:** 40.2%")
    
    st.markdown("---")
    st.markdown("*Health sector analysis | Pakistan Data Twin Dashboard*")