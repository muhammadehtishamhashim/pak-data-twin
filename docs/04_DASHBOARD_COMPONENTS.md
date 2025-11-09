# Dashboard Components

## 🎨 Overview

This document details all components of the Pakistan Data Twin Dashboard, including design, functionality, and implementation.

## 🏠 Landing Page

### Design Philosophy

The landing page serves as the entry point, providing:
- **First Impression**: Professional, modern design
- **Overview**: Quick stats and features
- **Call-to-Action**: Prominent "GET STARTED" button
- **Visual Appeal**: Animated elements and smooth transitions

### Components

#### 1. Welcome Container

**Features**:
- Light green gradient background
- Pakistan flag emoji
- Title and subtitle
- Description text
- Minimal green borders (4px left/right)
- Border radius: 20px
- Box shadow with 50% opacity

**Styling**:
```css
background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
border-left: 4px solid #0f4c3a;
border-right: 4px solid #0f4c3a;
border-radius: 20px;
box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
```

#### 2. GET STARTED Button

**Features**:
- Green gradient background
- Rounded corners (50px)
- Hover animation (lift + scale)
- Sweeping light effect (45° angle)
- Smooth transitions

**Animations**:
```css
/* Hover Effect */
transform: translateY(-3px) scale(1.05);

/* Sweeping Light */
animation: sweep 3s infinite;
```

#### 3. Background Elements

**Blurred Circles**:
- 5 large circles across the page
- Different sizes (180px - 300px)
- Various green shades
- 60px blur effect
- Floating animation (20s cycle)
- z-index: -1

**Data Particles**:
- 10 small dots (8px)
- Scattered positioning
- Float upward animation
- Scale and opacity changes
- 15s animation cycle

**Pulsing Rings**:
- 4 circular rings
- Expand and fade effect
- 3s pulse cycle
- Different sizes and positions

#### 4. Pakistan at a Glance

**Visualizations**:
- Population distribution (Pie chart)
- GDP contribution by province (Bar chart)
- Interactive Plotly charts
- Hover tooltips

#### 5. Feature Cards

**Layout**: 2x2 grid

**Sectors**:
1. Economy Dashboard
2. Education Dashboard
3. Energy Dashboard
4. Health Dashboard

**Styling**:
- White background
- Left border (3px green)
- Box shadow
- Hover lift effect
- Icon, title, description

#### 6. Technology Stack

**Display**: 4 columns

**Technologies**:
1. LSTM (with logo)
2. Plotly (with logo)
3. Python (with logo)
4. Streamlit (with logo)

**Logo Sizing**: 60px height, auto width

---

## 📊 Economy Dashboard

### Layout Structure

```
Economy Dashboard
├── Key Metrics Row (4 columns)
├── GDP Analysis (2 columns)
│   ├── GDP Trend Chart
│   └── Growth Rate Chart
├── GDP Sectoral Composition (Full width)
├── Trade & Exchange (2 columns)
│   ├── Exports & Remittances
│   └── Exchange Rates & Imports
├── Government Debt Analysis (Full width)
├── Foreign Investment (Full width)
├── Net Export Balance (Full width)
├── Sectoral Analysis (2 columns)
│   ├── Agriculture & Services
│   └── CPI & Commodities
└── Economic Overview Dashboard (Full width)
```

### Key Metrics

**Displayed Metrics**:
1. **GDP**: Latest value in billions USD
2. **Exports**: Latest monthly value
3. **Remittances**: Latest monthly value
4. **FDI**: Latest foreign investment

**Implementation**:
```python
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("GDP", f"${gdp_latest:.1f}B", "Current")
```

### Visualizations

#### 1. GDP Trend Chart
- **Type**: Line chart with markers
- **Data**: 1999-2025
- **Y-axis**: GDP in billions USD
- **Features**: Hover tooltips, zoom, pan

#### 2. GDP Growth Rate
- **Type**: Bar chart
- **Colors**: Green (positive), Red (negative)
- **Data**: Annual growth rates
- **Source**: Real GDP growth

#### 3. GDP Sectoral Composition
- **Type**: Donut chart
- **Sectors**: 4 major sectors
- **Features**: Percentage labels, hover info
- **Year**: 2025 (latest)

#### 4. Trade Analysis
- **Exports**: Area chart
- **Remittances**: Line chart
- **Exchange Rates**: Multi-line (NEER vs REER)
- **Imports**: Bar chart (recent 20 months)

#### 5. Debt Analysis
- **Type**: Subplots (2 rows, 2 columns)
- **Main Plot**: Total debt (full width)
- **Subplots**: 
  - Gross public debt
  - Domestic debt
  - External debt
- **Unit**: Trillion PKR

#### 6. Economic Overview
- **Type**: 2x2 subplot grid
- **Charts**: GDP, Trade, Investment, Inflation
- **Purpose**: Quick overview

### AI Forecasts Tab

**Forecasts Displayed**:
1. GDP LSTM Forecast (2026-2035)
2. Debt Forecast
3. Service Exports Forecast
4. Commodities Export Forecast

**Features**:
- Pre-generated JSON plots
- Interactive Plotly charts
- Success/error messages
- Expandable methodology section

---

## 🎓 Education Dashboard

### Layout Structure

```
Education Dashboard
├── Key Metrics Row (4 columns)
├── Tab Navigation
│   ├── Faculty Overview
│   ├── Universities
│   └── Geographic Distribution
└── Summary Statistics (3 columns)
```

### Key Metrics

1. **Total Faculty**: Computer science faculty count
2. **Universities**: Number of institutions
3. **PhD Holders**: Count and percentage
4. **Provinces**: Geographic coverage

### Tab 1: Faculty Overview

**Visualizations**:
1. **Terminal Degree Distribution**: Pie chart (top 8)
2. **Designation Distribution**: Bar chart
3. **Academic Hierarchy**: Horizontal bar chart
4. **Qualification Summary**: Donut chart

### Tab 2: Universities

**Visualizations**:
1. **Top 15 Universities**: Bar chart by faculty count
2. **University Statistics**: 3 metric cards

### Tab 3: Geographic Distribution

**Visualizations**:
1. **Province Distribution**: Bar chart
2. **Country of Graduation**: Bar chart (top 10)
3. **Cross-Analysis**: Grouped bar chart (degree vs province)

### Summary Statistics

**Sections**:
1. Geographic Coverage
2. Top Qualifications
3. Academic Positions

---

## ⚡ Energy Dashboard

**Status**: Placeholder implementation

**Planned Features**:
- Energy production charts
- Consumption patterns
- Renewable energy tracking
- Power generation capacity

---

## 🏥 Health Dashboard

**Status**: Placeholder implementation

**Planned Features**:
- Healthcare indicators
- Disease prevalence
- Hospital infrastructure
- Public health trends

---

## 🎨 Design System

### Color Palette

**Primary Colors**:
- Pakistan Green: `#0f4c3a`
- Light Green: `#e8f5e9`
- Medium Green: `#1a7f5f`
- Accent Green: `#2ea87e`

**Secondary Colors**:
- White: `#ffffff`
- Light Gray: `#f5f7fa`
- Dark Gray: `#333333`
- Text Gray: `#666666`

### Typography

**Fonts**:
- Primary: Sans-serif
- Sizes:
  - H1: 3rem (48px)
  - H2: 1.5rem (24px)
  - H3: 1.2rem (19px)
  - Body: 1rem (16px)
  - Small: 0.85rem (14px)

### Spacing

**Padding**:
- Container: 3rem 2rem
- Card: 1.5rem
- Button: 0.8rem 2rem

**Margins**:
- Section: 2rem auto
- Element: 1rem

### Shadows

**Box Shadows**:
- Light: `0 2px 8px rgba(0,0,0,0.1)`
- Medium: `0 4px 15px rgba(0,0,0,0.15)`
- Heavy: `0 0 40px rgba(0,0,0,0.5)`

### Animations

**Durations**:
- Fast: 0.3s
- Medium: 1s
- Slow: 3s
- Very Slow: 15-20s

**Easing**:
- Default: ease
- Smooth: ease-in-out
- Bounce: cubic-bezier

---

## 🔧 Component Implementation

### Streamlit Components

**Layout**:
```python
# Columns
col1, col2, col3 = st.columns(3)

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

# Expander
with st.expander("More Info"):
    st.write("Content")
```

**Widgets**:
```python
# Button
if st.button("Click Me"):
    # Action

# Metric
st.metric("Label", "Value", "Delta")

# Markdown
st.markdown("**Bold Text**")
```

### Plotly Charts

**Basic Chart**:
```python
fig = px.line(df, x='Date', y='Value', title='Chart Title')
st.plotly_chart(fig, use_container_width=True)
```

**Customization**:
```python
fig.update_layout(
    template="plotly_white",
    height=400,
    hovermode='x unified'
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
)
```

---

## 📱 Responsive Design

### Breakpoints

- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

### Adaptations

**Desktop**:
- Full sidebar
- Multi-column layouts
- Large charts

**Tablet**:
- Collapsible sidebar
- 2-column layouts
- Medium charts

**Mobile**:
- Hidden sidebar
- Single column
- Compact charts

---

## ♿ Accessibility

### Features

1. **Keyboard Navigation**: Tab through elements
2. **Screen Reader Support**: ARIA labels
3. **Color Contrast**: WCAG AA compliant
4. **Alt Text**: Images and icons
5. **Focus Indicators**: Visible focus states

### Best Practices

- Semantic HTML
- Descriptive labels
- Logical tab order
- Error messages
- Loading states

---

## 🔄 State Management

### Session State Variables

```python
# Navigation
st.session_state.show_landing = True
st.session_state.current_page = 'Economy'

# Data caching
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')
```

### Page Transitions

```python
# Scroll to top
st.markdown("""
<script>
    window.parent.document.querySelector('section.main').scrollTo(0, 0);
</script>
""", unsafe_allow_html=True)

# Rerun
st.rerun()
```

---

## 🎯 Performance Optimization

### Techniques

1. **Data Caching**: `@st.cache_data`
2. **Lazy Loading**: Load data on demand
3. **Image Optimization**: Compressed assets
4. **Code Splitting**: Modular structure
5. **Minimal Reruns**: Efficient state management

### Loading Times

- **Landing Page**: < 1s
- **Dashboard Load**: < 2s
- **Chart Render**: < 0.5s
- **Page Switch**: < 0.3s

---

**Next**: [Installation & Setup](05_INSTALLATION_SETUP.md)
