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
        <div class="welcome-flag">
            <img src="https://png.pngtree.com/recommend-works/png-clipart/20250705/ourmid/pngtree-artistic-brush-stroke-style-pakistan-flag-illustration-png-image_16607058.webp" 
                 style="height: 110px; width: auto; object-fit: contain; margin: 0 auto; display: block;" 
                 alt="Pakistan Flag">
        </div>
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
        if st.button("GET STARTED", use_container_width=True, type="primary", key="get_started"):
            st.session_state.show_landing = False
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Sources Section
    st.markdown('<h3 style="text-align: center; color: #0f4c3a; font-size: 1.8rem; margin: 2rem 0; font-weight: 700;">Data Sources & Partners</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            st.markdown("""
                <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <img src="https://pbs.twimg.com/profile_images/3369614509/cd253064339c502f469ff6ba49f0fc7e_400x400.png" 
                         style="height: 80px; width: auto; object-fit: contain; margin-bottom: 1rem;" 
                         alt="Pakistan Bureau of Statistics">
                    <div style="font-weight: 700; color: #0f4c3a; font-size: 0.95rem; margin-bottom: 0.3rem;">Pakistan Bureau of Statistics</div>
                    <div style="font-size: 0.75rem; color: #666; font-style: italic;">"Faith, Unity, Discipline"</div>
                </div>
            """, unsafe_allow_html=True)
        
        with subcol2:
            st.markdown("""
                <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT72BIjHaaWlfAIHYO9dkB-fwTETsSCYkEhfQ&s" 
                         style="height: 80px; width: auto; object-fit: contain; margin-bottom: 1rem;" 
                         alt="Ministry of Planning">
                    <div style="font-weight: 700; color: #0f4c3a; font-size: 0.95rem; margin-bottom: 0.3rem;">Ministry of Planning, Development & Special Initiatives</div>
                    <div style="font-size: 0.75rem; color: #666; font-style: italic;">"Building Pakistan's Future"</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Pakistan Data Visualization
    st.markdown("### 📊 Pakistan at a Glance")
    
    # Load actual datasets
    import pandas as pd
    
    # Load GDP data
    gdp_df = pd.read_csv('datasets_cleaned/Economy/Pakistan_GDP_2000-2025.csv')
    gdp_total = gdp_df[gdp_df['Series name'] == 'Gross Domestic Product (Total of Gross Value Addition at Constant Basic Prices(2015-16))'].copy()
    gdp_total['Year'] = pd.to_datetime(gdp_total['Observation Date']).dt.year
    gdp_total['GDP_Trillion'] = gdp_total['Observation Value'] / 1000000  # Convert to trillion PKR
    
    # Load enrollment data
    enrollment_df = pd.read_csv('datasets_cleaned/Education/Enrollments/5_year_enrollment.csv')
    
    # Get sector-wise enrollment for latest year (2023-24)
    sectors = ['Public', 'Other Public', 'Private']
    enrollment_2024 = enrollment_df[enrollment_df['Stage'] == 'Total'][['Sector', '2023-24']].copy()
    enrollment_2024 = enrollment_2024[enrollment_2024['Sector'].isin(sectors)]
    enrollment_2024['Enrollment_Millions'] = enrollment_2024['2023-24'] / 1000000
    
    # Get stage-wise enrollment trends
    stages = ['Primary', 'Middle', 'High', 'Higher Secondary/Inter Colleges', 'Universities']
    stage_trends = enrollment_df[enrollment_df['Stage'].isin(stages) & (enrollment_df['Sector'] == 'Total')]
    
    # Create 4 visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Pakistan GDP Growth (2000-2025)',
            'Education Enrollment by Sector (2023-24)',
            'GDP Sector Contribution (2025)',
            'Student Enrollment Trends by Stage'
        ),
        specs=[
            [{"type": "scatter"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "scatter"}]
        ],
        vertical_spacing=0.18,
        horizontal_spacing=0.1
    )
    
    # 1. GDP Growth Line Chart
    fig.add_trace(
        go.Scatter(
            x=gdp_total['Year'],
            y=gdp_total['GDP_Trillion'],
            mode='lines+markers',
            name='GDP',
            line=dict(color='#0f4c3a', width=3),
            marker=dict(size=6),
            hovertemplate="<b>Year: %{x}</b><br>GDP: %{y:.2f} Trillion PKR<extra></extra>"
        ),
        row=1, col=1
    )
    
    # 2. Enrollment by Sector Pie Chart
    fig.add_trace(
        go.Pie(
            labels=enrollment_2024['Sector'],
            values=enrollment_2024['Enrollment_Millions'],
            hole=0.4,
            marker=dict(colors=['#0f4c3a', '#2ea87e', '#7ee5c7']),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Students: %{value:.2f}M<br>Share: %{percent}<extra></extra>"
        ),
        row=1, col=2
    )
    
    # 3. GDP Sector Contribution Bar Chart (2025 data)
    gdp_sectors_2025 = gdp_df[gdp_df['Observation Date'] == '2025-06-30']
    sector_data = gdp_sectors_2025[gdp_sectors_2025['Series name'].isin([
        'Agricultural Sector', 'Industrial Sector', 'Services Sector'
    ])].copy()
    sector_data['Value_Trillion'] = sector_data['Observation Value'] / 1000000
    sector_names = ['Agriculture', 'Industry', 'Services']
    
    fig.add_trace(
        go.Bar(
            x=sector_names,
            y=sector_data['Value_Trillion'].values,
            marker=dict(
                color=['#0f4c3a', '#2ea87e', '#7ee5c7'],
                line=dict(color='#0f4c3a', width=1)
            ),
            text=[f'{x:.1f}T' for x in sector_data['Value_Trillion'].values],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Contribution: %{y:.2f} Trillion PKR<extra></extra>"
        ),
        row=2, col=1
    )
    
    # 4. Enrollment Trends by Stage
    years = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    colors = ['#0f4c3a', '#1a7f5f', '#2ea87e', '#4fd1a8', '#7ee5c7']
    
    for idx, stage in enumerate(stages):
        stage_data = stage_trends[stage_trends['Stage'] == stage]
        values = [stage_data[year].values[0] / 1000000 for year in years]
        
        fig.add_trace(
            go.Scatter(
                x=years,
                y=values,
                mode='lines+markers',
                name=stage,
                line=dict(color=colors[idx], width=2),
                marker=dict(size=5),
                hovertemplate=f"<b>{stage}</b><br>Year: %{{x}}<br>Students: %{{y:.2f}}M<extra></extra>"
            ),
            row=2, col=2
        )
    
    # Update layout
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_yaxes(title_text="GDP (Trillion PKR)", row=1, col=1)
    
    fig.update_xaxes(title_text="Sector", row=2, col=1)
    fig.update_yaxes(title_text="Contribution (Trillion PKR)", row=2, col=1)
    
    fig.update_xaxes(title_text="Academic Year", row=2, col=2)
    fig.update_yaxes(title_text="Students (Millions)", row=2, col=2)
    
    fig.update_layout(
        height=700,
        showlegend=True,
        template="plotly_white",
        font=dict(size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
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
    st.markdown("### Technology Stack")
    
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
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6UTPV9TTPThzYSFv8Ps9o4hdlr84SRn_f5g&s" 
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
            Pakistan Data Twin Dashboard © 2025 | Built with ❤️ for Pakistan
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
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; margin: 0; padding: 0;">
        <img src="https://png.pngtree.com/recommend-works/png-clipart/20250705/ourmid/pngtree-artistic-brush-stroke-style-pakistan-flag-illustration-png-image_16607058.webp" 
             style="height: 40px; width: auto; object-fit: contain; margin: 0 10px 0 0;" 
             alt="Pakistan Flag">
        <h1 style="margin: 0; padding: 0; font-size: 1.1rem; font-weight: 700;">PAKISTAN DATA TWIN</h1>
    </div>
    """, unsafe_allow_html=True)
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