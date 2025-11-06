import streamlit as st

# Import dashboard pages
from dashboard_pages import economy, education, energy, health

# Page configuration
st.set_page_config(
    page_title="Pakistan Data Twin Dashboard",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Economy'

# Sidebar
st.sidebar.title("🇵🇰 PAKISTAN DATA TWIN")
st.sidebar.markdown("---")

# Navigation buttons
if st.sidebar.button("ECONOMY", use_container_width=True):
    st.session_state.current_page = 'Economy'

if st.sidebar.button("EDUCATION", use_container_width=True):
    st.session_state.current_page = 'Education'

if st.sidebar.button("ENERGY", use_container_width=True):
    st.session_state.current_page = 'Energy'

if st.sidebar.button("HEALTH", use_container_width=True):
    st.session_state.current_page = 'Health'

# Page routing
if st.session_state.current_page == 'Economy':
    economy.show()
elif st.session_state.current_page == 'Education':
    education.show()
elif st.session_state.current_page == 'Energy':
    energy.show()
elif st.session_state.current_page == 'Health':
    health.show()

# Footer
st.markdown("---")
st.markdown("*Pakistan Data Twin Dashboard | Built with Streamlit*")