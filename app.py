import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import dashboard pages
from dashboard_pages import economy, education, energy, health

# Page configuration
st.set_page_config(
    page_title="Pakistan Data Twin Dashboard",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Economy'

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide sidebar initially */
    [data-testid="stSidebar"] {display: none;}
    
    /* Background decorative circles */
    .bg-circles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
        pointer-events: none;
    }
    
    .circle {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.3;
        animation: float 20s infinite ease-in-out;
    }
    
    .circle1 {
        width: 300px;
        height: 300px;
        background: #0f4c3a;
        top: 10%;
        left: 5%;
        animation-delay: 0s;
    }
    
    .circle2 {
        width: 200px;
        height: 200px;
        background: #1a7f5f;
        top: 60%;
        right: 10%;
        animation-delay: 3s;
    }
    
    .circle3 {
        width: 250px;
        height: 250px;
        background: #2ea87e;
        bottom: 15%;
        left: 15%;
        animation-delay: 6s;
    }
    
    .circle4 {
        width: 180px;
        height: 180px;
        background: #4fd1a8;
        top: 30%;
        right: 20%;
        animation-delay: 9s;
    }
    
    .circle5 {
        width: 220px;
        height: 220px;
        background: #7ee5c7;
        bottom: 40%;
        left: 40%;
        animation-delay: 12s;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        25% {
            transform: translate(30px, -30px) scale(1.1);
        }
        50% {
            transform: translate(-20px, 20px) scale(0.9);
        }
        75% {
            transform: translate(20px, 30px) scale(1.05);
        }
    }
    
    /* Welcome container styling */
    .welcome-container {
        position: relative;
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 4px solid #0f4c3a;
        border-right: 4px solid #0f4c3a;
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 900px;
        text-align: center;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
        overflow: hidden;
    }
    
    /* Blurred circles inside welcome container */
    .welcome-container::before,
    .welcome-container::after {
        content: '';
        position: absolute;
        border-radius: 50%;
        filter: blur(40px);
        opacity: 0.4;
        z-index: 0;
    }
    
    .welcome-container::before {
        width: 200px;
        height: 200px;
        background: #4fd1a8;
        top: -50px;
        right: -50px;
    }
    
    .welcome-container::after {
        width: 150px;
        height: 150px;
        background: #7ee5c7;
        bottom: -30px;
        left: -30px;
    }
    
    .welcome-flag {
        position: relative;
        z-index: 1;
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        position: relative;
        z-index: 1;
        font-size: 3rem;
        font-weight: 800;
        color: #0f4c3a;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        position: relative;
        z-index: 1;
        font-size: 1.3rem;
        color: #2d5f3f;
        margin-bottom: 1.5rem;
    }
    
    .welcome-description {
        position: relative;
        z-index: 1;
        font-size: 1rem;
        color: #1a4d2e;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        position: relative;
        background: linear-gradient(135deg, #0f4c3a 0%, #1a7f5f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(15, 76, 58, 0.3) !important;
    }
    
    /* Sweeping light animation */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transform: rotate(45deg);
        animation: sweep 3s infinite;
    }
    
    @keyframes sweep {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    /* Hover effect */
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(15, 76, 58, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
        border-left: 3px solid #0f4c3a;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f4c3a;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.5;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Landing Page
if st.session_state.show_landing:
    # Background decorative circles
    st.markdown("""
    <div class="bg-circles">
        <div class="circle circle1"></div>
        <div class="circle circle2"></div>
        <div class="circle circle3"></div>
        <div class="circle circle4"></div>
        <div class="circle circle5"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Container
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-flag">🇵🇰</div>
        <h1 class="welcome-title">PAKISTAN DATA TWIN</h1>
        <p class="welcome-subtitle">Intelligent Analytics for a Digital Pakistan</p>
        <p class="welcome-description">
            Explore comprehensive data-driven insights across Economy, Education, Energy, and Health sectors. 
            Powered by advanced AI and machine learning models to forecast Pakistan's future.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Started Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 GET STARTED", use_container_width=True, type="primary", key="get_started"):
            st.session_state.show_landing = False
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Pakistan Map Visualization
    st.markdown("### 🗺️ Pakistan at a Glance")
    
    # Sample data for provinces
    provinces = ['Punjab', 'Sindh', 'KPK', 'Balochistan', 'Capital']
    population = [110, 48, 35, 12, 2]  # in millions
    gdp_contribution = [53, 28, 11, 4, 4]  # percentage
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Population Distribution', 'GDP Contribution by Province'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Population pie chart
    fig.add_trace(
        go.Pie(
            labels=provinces,
            values=population,
            hole=0.4,
            marker=dict(colors=['#0f4c3a', '#1a7f5f', '#2ea87e', '#4fd1a8', '#7ee5c7']),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Population: %{value}M<br>Share: %{percent}<extra></extra>"
        ),
        row=1, col=1
    )
    
    # GDP bar chart
    fig.add_trace(
        go.Bar(
            x=provinces,
            y=gdp_contribution,
            marker=dict(
                color=gdp_contribution,
                colorscale='Greens',
                showscale=False
            ),
            text=[f'{x}%' for x in gdp_contribution],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>GDP Share: %{y}%<extra></extra>"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        template="plotly_white",
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Features Section
    st.markdown("### 🎯 Explore Our Dashboards")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Economy Dashboard</div>
            <div class="feature-description">
                Comprehensive economic analysis including GDP trends, trade balance, debt analysis, 
                foreign investment, and AI-powered forecasts.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-top: 1rem;">
            <div class="feature-icon">🎓</div>
            <div class="feature-title">Education Dashboard</div>
            <div class="feature-description">
                Analyze faculty distribution, university rankings, qualification trends, 
                and geographic spread of educational institutions.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Energy Dashboard</div>
            <div class="feature-description">
                Track energy production, consumption patterns, renewable energy adoption, 
                and power generation capacity.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-top: 1rem;">
            <div class="feature-icon">🏥</div>
            <div class="feature-title">Health Dashboard</div>
            <div class="feature-description">
                Monitor healthcare indicators, disease prevalence, hospital infrastructure, 
                and public health trends.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("### 🚀 Technology Stack")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUs5FO2feoa0-blYnAqb3gqGv-IoOFdEReOQ&s" 
                 style="height: 60px; width: auto; object-fit: contain; margin-bottom: 0.5rem;" 
                 alt="LSTM">
            <div style="font-weight: 600; color: #0f4c3a; font-size: 0.85rem;">LSTM</div>
            <div style="font-size: 0.7rem; color: #666;">(Long Short-Term Memory)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <img src="https://ml.globenewswire.com/Resource/Download/54ca9baa-43ae-4b0d-bcc3-5dcde3ab7ce0?size=2" 
                 style="height: 60px; width: auto; object-fit: contain; margin-bottom: 0.5rem;" 
                 alt="Plotly">
            <div style="font-weight: 600; color: #0f4c3a; font-size: 0.9rem;">Plotly</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <img src="https://www.citypng.com/public/uploads/preview/hd-python-logo-symbol-transparent-png-735811696257415dbkifcuokn.png" 
                 style="height: 60px; width: auto; object-fit: contain; margin-bottom: 0.5rem;" 
                 alt="Python">
            <div style="font-weight: 600; color: #0f4c3a; font-size: 0.9rem;">Python</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <img src="https://images.seeklogo.com/logo-png/44/2/streamlit-logo-png_seeklogo-441815.png" 
                 style="height: 60px; width: auto; object-fit: contain; margin-bottom: 0.5rem;" 
                 alt="Streamlit">
            <div style="font-weight: 600; color: #0f4c3a; font-size: 0.9rem;">Streamlit</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <p style="font-size: 0.9rem;">
            Pakistan Data Twin Dashboard © 2024 | Built with ❤️ for Pakistan
        </p>
        <p style="font-size: 0.8rem; color: #999;">
            Empowering data-driven decisions for a better tomorrow
        </p>
    </div>
    """, unsafe_allow_html=True)

# Dashboard
else:
    # Show sidebar for dashboard navigation
    st.markdown('<style>[data-testid="stSidebar"] {display: block !important;}</style>', unsafe_allow_html=True)
    
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
    
    # Back to landing page button
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 BACK TO HOME", use_container_width=True):
        st.session_state.show_landing = True
        st.rerun()
    
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