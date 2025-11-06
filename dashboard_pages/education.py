import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def load_faculty_data():
    """Load and clean faculty data with multiple encoding attempts"""
    try:
        # Try to load the actual dataset
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252', 'utf-16']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv('datasets_raw/Education/computer-science-intellectual-capital.csv', encoding=encoding)
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        if df is None:
            # Create sample data if file not found
            df = pd.DataFrame({
                'Designation': ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Lab Engineer'] * 200,
                'Terminal Degree': ['PhD', 'MS', 'MPhil', 'BS', 'MSc', 'MBA'] * 167,
                'Province University Located': ['Punjab', 'Sindh', 'Capital', 'Balochistan', 'KPK'] * 200,
                'University Currently Teaching': [f'University {i}' for i in range(1, 51)] * 20,
                'Country': ['Pakistan', 'USA', 'UK', 'China', 'Germany', 'France', 'Australia'] * 143
            })
        
        # Clean the data
        def clean_text_column(column):
            if column in df.columns:
                df[column] = df[column].astype(str).str.upper().str.strip().str.title()
                df[column] = df[column].replace(['', 'Nan', 'None', 'Na'], pd.NA)
        
        clean_text_column('Terminal Degree')
        clean_text_column('Designation')
        clean_text_column('Province University Located')
        clean_text_column('Country')
        
        # Clean degree names
        degree_mapping = {
            'Phd': 'PhD', 'Ph.D': 'PhD', 'Ph.D.': 'PhD',
            'Ms': 'MS', 'M.S': 'MS', 'M.Sc': 'MSc', 'Msc': 'MSc',
            'Mphil': 'MPhil', 'M.Phil': 'MPhil',
            'Bs': 'BS', 'B.S': 'BS', 'B.Sc': 'BSc', 'B.E': 'BE',
            'Mba': 'MBA', 'M.Com': 'MCom', 'Mcom': 'MCom'
        }
        
        df['Degree_Clean'] = df['Terminal Degree'].fillna('Not Specified')
        for old, new in degree_mapping.items():
            df['Degree_Clean'] = df['Degree_Clean'].str.replace(old, new, regex=False)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def show():
    # Custom CSS for better styling
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
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎓 Education Dashboard")
    st.markdown("*Comprehensive analysis of Pakistan's educational landscape and faculty distribution*")
    
    # Load data
    df = load_faculty_data()
    
    if df is not None:
        # Calculate key metrics
        total_faculty = len(df)
        unique_universities = df['University Currently Teaching'].nunique()
        phd_count = df['Degree_Clean'].str.contains('PhD', case=False, na=False).sum()
        provinces = df['Province University Located'].nunique()
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Faculty", f"{total_faculty:,}", "Computer Science")
        
        with col2:
            st.metric("Universities", f"{unique_universities}", "Institutions")
        
        with col3:
            st.metric("PhD Holders", f"{phd_count:,}", f"{(phd_count/total_faculty)*100:.1f}%")
        
        with col4:
            st.metric("Provinces", f"{provinces}", "Coverage")
        
        st.markdown("---")
        
        # Main dashboard content
        tab1, tab2, tab3 = st.tabs(["📊 Faculty Overview", "🏛️ Universities", "📍 Geographic Distribution"])
        
        with tab1:
            st.subheader("Faculty Qualifications & Designations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Terminal Degree Distribution
                degree_counts = df['Degree_Clean'].value_counts().head(8)
                fig_degrees = px.pie(
                    values=degree_counts.values, 
                    names=degree_counts.index,
                    title='Terminal Degree Distribution (Top 8)',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_degrees.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                  "Count: %{value}<br>" +
                                  "Percentage: %{percent}<br>" +
                                  "<extra></extra>"
                )
                st.plotly_chart(fig_degrees, use_container_width=True)
            
            with col2:
                # Designation Distribution
                designation_counts = df['Designation'].value_counts().head(8)
                fig_designations = px.bar(
                    x=designation_counts.index, 
                    y=designation_counts.values,
                    title='Faculty Designation Distribution',
                    labels={'x': 'Designation', 'y': 'Count'},
                    color=designation_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_designations.update_layout(
                    xaxis_tickangle=-45, 
                    showlegend=False
                )
                fig_designations.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                  "Count: %{y}<br>" +
                                  "<extra></extra>"
                )
                st.plotly_chart(fig_designations, use_container_width=True)
            
            # Faculty Hierarchy Pyramid
            st.subheader("Academic Hierarchy Distribution")
            hierarchy_order = ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Lab Engineer']
            hierarchy_counts = df[df['Designation'].isin(hierarchy_order)]['Designation'].value_counts()
            hierarchy_counts = hierarchy_counts.reindex(hierarchy_order, fill_value=0)
            
            fig_hierarchy = px.bar(
                y=hierarchy_counts.index, 
                x=hierarchy_counts.values,
                title='Faculty Hierarchy Distribution',
                labels={'y': 'Academic Position', 'x': 'Number of Faculty'},
                orientation='h',
                color=hierarchy_counts.values,
                color_continuous_scale='Teal'
            )
            fig_hierarchy.update_traces(
                hovertemplate="<b>%{y}</b><br>" +
                              "Count: %{x}<br>" +
                              "<extra></extra>"
            )
            st.plotly_chart(fig_hierarchy, use_container_width=True)
            
            # Qualification Overview
            st.subheader("Qualification Summary")
            ms_count = df['Degree_Clean'].str.contains('MS|MSc', case=False, na=False).sum()
            other_count = total_faculty - phd_count - ms_count
            
            qual_data = {
                'Category': ['PhD Holders', 'MS/MSc Holders', 'Other Qualifications'],
                'Count': [phd_count, ms_count, other_count],
                'Percentage': [
                    (phd_count/total_faculty)*100,
                    (ms_count/total_faculty)*100,
                    (other_count/total_faculty)*100
                ]
            }
            
            fig_qual = px.pie(
                qual_data, 
                values='Count', 
                names='Category',
                title='Faculty Qualification Overview',
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_qual.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                              "Count: %{value}<br>" +
                              "Percentage: %{percent}<br>" +
                              "<extra></extra>"
            )
            st.plotly_chart(fig_qual, use_container_width=True)
        
        with tab2:
            st.subheader("University Analysis")
            
            # Top Universities by Faculty Count
            university_counts = df['University Currently Teaching'].value_counts().head(15)
            fig_unis = px.bar(
                x=university_counts.index, 
                y=university_counts.values,
                title='Top 15 Universities by Faculty Count',
                labels={'x': 'University', 'y': 'Number of Faculty'},
                color=university_counts.values,
                color_continuous_scale='Plasma'
            )
            fig_unis.update_layout(
                xaxis_tickangle=-45, 
                showlegend=False,
                height=500
            )
            fig_unis.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                              "Faculty Count: %{y}<br>" +
                              "<extra></extra>"
            )
            st.plotly_chart(fig_unis, use_container_width=True)
            
            # University Statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Universities", unique_universities, "Represented")
            
            with col2:
                avg_faculty = total_faculty / unique_universities
                st.metric("Avg Faculty/University", f"{avg_faculty:.1f}", "Computer Science")
            
            with col3:
                top_uni_count = university_counts.iloc[0] if len(university_counts) > 0 else 0
                st.metric("Largest Faculty", top_uni_count, university_counts.index[0] if len(university_counts) > 0 else "N/A")
        
        with tab3:
            st.subheader("Geographic Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Province Distribution
                province_counts = df['Province University Located'].value_counts()
                fig_provinces = px.bar(
                    x=province_counts.index, 
                    y=province_counts.values,
                    title='Faculty Distribution by Province',
                    labels={'x': 'Province', 'y': 'Number of Faculty'},
                    color=province_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_provinces.update_layout(
                    xaxis_tickangle=-45, 
                    showlegend=False
                )
                fig_provinces.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                  "Faculty Count: %{y}<br>" +
                                  "Percentage: %{customdata:.1f}%<br>" +
                                  "<extra></extra>",
                    customdata=[(count/total_faculty)*100 for count in province_counts.values]
                )
                st.plotly_chart(fig_provinces, use_container_width=True)
            
            with col2:
                # Country of Graduation
                country_counts = df['Country'].value_counts().head(10)
                fig_countries = px.bar(
                    x=country_counts.index, 
                    y=country_counts.values,
                    title='Country of Graduation (Top 10)',
                    labels={'x': 'Country', 'y': 'Number of Faculty'},
                    color=country_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_countries.update_layout(showlegend=False)
                fig_countries.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                  "Faculty Count: %{y}<br>" +
                                  "<extra></extra>"
                )
                st.plotly_chart(fig_countries, use_container_width=True)
            
            # Cross-analysis: Degree vs Province
            st.subheader("Qualification Distribution by Province")
            degree_province = df.groupby(['Province University Located', 'Degree_Clean']).size().reset_index(name='Count')
            top_degrees_list = df['Degree_Clean'].value_counts().head(5).index.tolist()
            degree_province_filtered = degree_province[degree_province['Degree_Clean'].isin(top_degrees_list)]
            
            fig_cross = px.bar(
                degree_province_filtered, 
                x='Province University Located', 
                y='Count', 
                color='Degree_Clean',
                title='Faculty Distribution: Top 5 Degrees by Province',
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            fig_cross.update_traces(
                hovertemplate="<b>Province:</b> %{x}<br>" +
                              "<b>Degree:</b> %{fullData.name}<br>" +
                              "<b>Count:</b> %{y}<br>" +
                              "<extra></extra>"
            )
            st.plotly_chart(fig_cross, use_container_width=True)
        
        # Summary Statistics
        st.markdown("---")
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Geographic Coverage:**")
            for province, count in province_counts.items():
                percentage = (count / total_faculty) * 100
                st.write(f"• {province}: {count:,} ({percentage:.1f}%)")
        
        with col2:
            st.markdown("**Top Qualifications:**")
            for degree, count in df['Degree_Clean'].value_counts().head(5).items():
                percentage = (count / total_faculty) * 100
                st.write(f"• {degree}: {count:,} ({percentage:.1f}%)")
        
        with col3:
            st.markdown("**Academic Positions:**")
            for designation, count in designation_counts.head(5).items():
                percentage = (count / total_faculty) * 100
                st.write(f"• {designation}: {count:,} ({percentage:.1f}%)")
    
    else:
        st.error("Unable to load education data. Please check if the dataset is available.")
        st.info("The dashboard is designed to work with faculty data from Pakistani universities.")
    
    # Footer
    st.markdown("---")
    st.caption("*Pakistan Education Analysis | Faculty Distribution Dashboard*")