import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show():
    st.title("🎓 Education Dashboard")
    st.markdown("*Comprehensive analysis of Pakistan's education system - Enrollments and Teachers*")
    
    # Create tabs for Enrollments and Teachers
    tab1, tab2 = st.tabs(["📚 Student Enrollments", "👨‍🏫 Teachers"])
    
    with tab1:
        show_enrollment_analysis()
    
    with tab2:
        show_teacher_analysis()


def show_enrollment_analysis():
    """Display enrollment visualizations"""
    st.subheader("Student Enrollment Analysis")
    
    # Load enrollment data
    enrollment_5yr = pd.read_csv('datasets_cleaned/Education/Enrollments/5_year_enrollment.csv')
    enrollment_2024 = pd.read_csv('datasets_cleaned/Education/Enrollments/Total_enrollment_2023to2024.csv')
    enrollment_classwise = pd.read_csv('datasets_cleaned/Education/Enrollments/Enrollment_Class_Wise.csv')
    enrollment_10yr = pd.read_csv('datasets_cleaned/Education/Enrollments/Total_Enrollent(Public)_Ten_Years.csv')
    
    # Key Metrics
    total_students = enrollment_2024['TOTAL - Total'].sum()
    total_boys = enrollment_2024['TOTAL - Boys'].sum()
    total_girls = enrollment_2024['TOTAL - Girls'].sum()
    urban_students = enrollment_2024['URBAN - Total'].sum()
    rural_students = enrollment_2024['RURAL - Total'].sum()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Students", f"{total_students/1000000:.1f}M", "2023-24")
    with col2:
        st.metric("Boys", f"{total_boys/1000000:.1f}M", f"{(total_boys/total_students)*100:.1f}%")
    with col3:
        st.metric("Girls", f"{total_girls/1000000:.1f}M", f"{(total_girls/total_students)*100:.1f}%")
    with col4:
        st.metric("Urban", f"{urban_students/1000000:.1f}M", f"{(urban_students/total_students)*100:.1f}%")
    with col5:
        st.metric("Rural", f"{rural_students/1000000:.1f}M", f"{(rural_students/total_students)*100:.1f}%")
    
    st.markdown("---")
    
    # Row 1: Provincial Distribution and Gender Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Provincial enrollment distribution
        province_data = enrollment_2024[enrollment_2024['Stage'] == 'Total'][['Province/Region', 'TOTAL - Total']]
        province_data = province_data[province_data['Province/Region'] != 'Pakistan']
        
        fig_province = px.bar(
            province_data,
            x='Province/Region',
            y='TOTAL - Total',
            title='Student Enrollment by Province/Region (2023-24)',
            labels={'TOTAL - Total': 'Total Students', 'Province/Region': 'Province'},
            color='TOTAL - Total',
            color_continuous_scale='Greens'
        )
        fig_province.update_traces(
            text=province_data['TOTAL - Total'].apply(lambda x: f'{x/1000000:.1f}M'),
            textposition='outside'
        )
        fig_province.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_province, use_container_width=True)
    
    with col2:
        # Gender distribution by province
        gender_data = enrollment_2024[enrollment_2024['Stage'] == 'Total'][['Province/Region', 'TOTAL - Boys', 'TOTAL - Girls']]
        gender_data = gender_data[gender_data['Province/Region'] != 'Pakistan']
        
        fig_gender = go.Figure()
        fig_gender.add_trace(go.Bar(
            name='Boys',
            x=gender_data['Province/Region'],
            y=gender_data['TOTAL - Boys'],
            marker_color='#0f4c3a'
        ))
        fig_gender.add_trace(go.Bar(
            name='Girls',
            x=gender_data['Province/Region'],
            y=gender_data['TOTAL - Girls'],
            marker_color='#7ee5c7'
        ))
        fig_gender.update_layout(
            title='Gender Distribution by Province (2023-24)',
            barmode='group',
            xaxis_title='Province',
            yaxis_title='Number of Students',
            height=400
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    # Row 2: Stage-wise enrollment and Urban vs Rural
    col1, col2 = st.columns(2)
    
    with col1:
        # Stage-wise enrollment
        stages = ['Pre Primary', 'Primary', 'Middle', 'High', 'Higher Secondary', 'Degree']
        stage_data = enrollment_2024[enrollment_2024['Province/Region'] == 'Pakistan']
        stage_data = stage_data[stage_data['Stage'].isin(stages)]
        
        fig_stage = px.pie(
            stage_data,
            values='TOTAL - Total',
            names='Stage',
            title='Enrollment Distribution by Education Stage (2023-24)',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig_stage.update_traces(textinfo='label+percent')
        st.plotly_chart(fig_stage, use_container_width=True)
    
    with col2:
        # Urban vs Rural by stage
        urban_rural_data = enrollment_2024[enrollment_2024['Province/Region'] == 'Pakistan']
        urban_rural_data = urban_rural_data[urban_rural_data['Stage'].isin(stages)]
        
        fig_ur = go.Figure()
        fig_ur.add_trace(go.Bar(
            name='Urban',
            x=urban_rural_data['Stage'],
            y=urban_rural_data['URBAN - Total'],
            marker_color='#2ea87e'
        ))
        fig_ur.add_trace(go.Bar(
            name='Rural',
            x=urban_rural_data['Stage'],
            y=urban_rural_data['RURAL - Total'],
            marker_color='#0f4c3a'
        ))
        fig_ur.update_layout(
            title='Urban vs Rural Enrollment by Stage (2023-24)',
            barmode='stack',
            xaxis_title='Education Stage',
            yaxis_title='Number of Students',
            height=400
        )
        st.plotly_chart(fig_ur, use_container_width=True)
    
    # Row 3: 5-Year Trends
    st.subheader("Enrollment Trends (2019-2024)")
    
    # Prepare 5-year trend data
    years = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    trend_stages = ['Primary', 'Middle', 'High', 'Higher Secondary/Inter Colleges', 'Universities']
    trend_data = enrollment_5yr[enrollment_5yr['Stage'].isin(trend_stages) & (enrollment_5yr['Sector'] == 'Total')]
    
    fig_trend = go.Figure()
    colors = ['#0f4c3a', '#1a7f5f', '#2ea87e', '#4fd1a8', '#7ee5c7']
    
    for idx, stage in enumerate(trend_stages):
        stage_row = trend_data[trend_data['Stage'] == stage]
        values = [stage_row[year].values[0] / 1000000 for year in years]
        
        fig_trend.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            name=stage,
            line=dict(color=colors[idx], width=3),
            marker=dict(size=8)
        ))
    
    fig_trend.update_layout(
        title='5-Year Enrollment Trends by Education Stage',
        xaxis_title='Academic Year',
        yaxis_title='Students (Millions)',
        height=450,
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Row 4: Sector-wise distribution (Public vs Private)
    col1, col2 = st.columns(2)
    
    with col1:
        # Sector distribution pie chart
        sector_data = enrollment_5yr[enrollment_5yr['Stage'] == 'Total'][['Sector', '2023-24']]
        sector_data = sector_data[sector_data['Sector'].isin(['Public', 'Private', 'Other Public'])]
        
        fig_sector = px.pie(
            sector_data,
            values='2023-24',
            names='Sector',
            title='Enrollment by Sector (2023-24)',
            hole=0.4,
            color_discrete_sequence=['#0f4c3a', '#7ee5c7', '#2ea87e']
        )
        fig_sector.update_traces(textinfo='label+percent')
        st.plotly_chart(fig_sector, use_container_width=True)
    
    with col2:
        # Class-wise enrollment
        class_data = enrollment_classwise[enrollment_classwise['Stage'] != 'Grand Total']
        class_totals = class_data.groupby('Stage')['Total - Total'].sum().reset_index()
        
        fig_class = px.bar(
            class_totals,
            x='Stage',
            y='Total - Total',
            title='Total Enrollment by Stage (All Sectors)',
            labels={'Total - Total': 'Total Students', 'Stage': 'Education Stage'},
            color='Total - Total',
            color_continuous_scale='Teal'
        )
        fig_class.update_traces(
            text=class_totals['Total - Total'].apply(lambda x: f'{x/1000000:.1f}M'),
            textposition='outside'
        )
        fig_class.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_class, use_container_width=True)


def show_teacher_analysis():
    """Display teacher visualizations"""
    st.subheader("Teacher Distribution Analysis")
    
    # Load teacher data
    teachers_provincial = pd.read_csv('datasets_cleaned/Education/Teachers/Teachers_Total_Provincial.csv')
    teachers_academic = pd.read_csv('datasets_cleaned/Education/Teachers/Teacher_Academic_Qualification_Total(Public Sector).csv')
    teachers_professional = pd.read_csv('datasets_cleaned/Education/Teachers/Teacher_Professional_Qualification_Total(Public Sector).csv')
    teachers_5yr = pd.read_csv('datasets_cleaned/Education/Teachers/5_year_Teachers.csv')
    
    # Key Metrics
    total_teachers = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']['TOTAL Total'].sum()
    male_teachers = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']['TOTAL Male'].sum()
    female_teachers = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']['TOTAL Female'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teachers", f"{total_teachers:,}", "All Levels")
    with col2:
        st.metric("Male Teachers", f"{male_teachers:,}", f"{(male_teachers/total_teachers)*100:.1f}%")
    with col3:
        st.metric("Female Teachers", f"{female_teachers:,}", f"{(female_teachers/total_teachers)*100:.1f}%")
    with col4:
        gender_ratio = female_teachers / male_teachers
        st.metric("Female:Male Ratio", f"1:{gender_ratio:.2f}", "Gender Balance")
    
    st.markdown("---")
    
    # Row 1: Provincial distribution and Gender distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Provincial teacher distribution
        province_teachers = teachers_provincial[teachers_provincial['Province/Region'] != 'Pakistan']
        province_totals = province_teachers.groupby('Province/Region')['TOTAL Total'].sum().reset_index()
        
        fig_prov = px.bar(
            province_totals,
            x='Province/Region',
            y='TOTAL Total',
            title='Teacher Distribution by Province/Region',
            labels={'TOTAL Total': 'Number of Teachers', 'Province/Region': 'Province'},
            color='TOTAL Total',
            color_continuous_scale='Greens'
        )
        fig_prov.update_traces(
            text=province_totals['TOTAL Total'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        )
        fig_prov.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_prov, use_container_width=True)
    
    with col2:
        # Gender distribution by province
        gender_prov = teachers_provincial[teachers_provincial['Province/Region'] != 'Pakistan']
        gender_prov_totals = gender_prov.groupby('Province/Region')[['TOTAL Male', 'TOTAL Female']].sum().reset_index()
        
        fig_gender_prov = go.Figure()
        fig_gender_prov.add_trace(go.Bar(
            name='Male',
            x=gender_prov_totals['Province/Region'],
            y=gender_prov_totals['TOTAL Male'],
            marker_color='#0f4c3a'
        ))
        fig_gender_prov.add_trace(go.Bar(
            name='Female',
            x=gender_prov_totals['Province/Region'],
            y=gender_prov_totals['TOTAL Female'],
            marker_color='#7ee5c7'
        ))
        fig_gender_prov.update_layout(
            title='Gender Distribution of Teachers by Province',
            barmode='group',
            xaxis_title='Province',
            yaxis_title='Number of Teachers',
            height=400
        )
        st.plotly_chart(fig_gender_prov, use_container_width=True)
    
    # Row 2: Level-wise distribution and Urban vs Rural
    col1, col2 = st.columns(2)
    
    with col1:
        # Teachers by education level
        pakistan_data = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']
        levels = ['Pre-Primary', 'Primary', 'Middle', 'High', 'Higher Secondary', 'Degree Colleges']
        level_data = pakistan_data[pakistan_data['Level'].isin(levels)]
        
        fig_level = px.pie(
            level_data,
            values='TOTAL Total',
            names='Level',
            title='Teacher Distribution by Education Level',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig_level.update_traces(textinfo='label+percent')
        st.plotly_chart(fig_level, use_container_width=True)
    
    with col2:
        # Urban vs Rural teachers
        urban_rural = pakistan_data[pakistan_data['Level'].isin(levels)]
        
        fig_ur_teachers = go.Figure()
        fig_ur_teachers.add_trace(go.Bar(
            name='Urban',
            x=urban_rural['Level'],
            y=urban_rural['URBAN Total'],
            marker_color='#2ea87e'
        ))
        fig_ur_teachers.add_trace(go.Bar(
            name='Rural',
            x=urban_rural['Level'],
            y=urban_rural['RURAL Total'],
            marker_color='#0f4c3a'
        ))
        fig_ur_teachers.update_layout(
            title='Urban vs Rural Teachers by Level',
            barmode='stack',
            xaxis_title='Education Level',
            yaxis_title='Number of Teachers',
            height=400
        )
        st.plotly_chart(fig_ur_teachers, use_container_width=True)
    
    # Row 3: Academic Qualifications
    st.subheader("Teacher Qualifications (Public Sector)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Academic qualifications
        academic_total = teachers_academic[teachers_academic['Level'] == 'Total']
        qual_data = academic_total[['Academic Qualification', 'Total Total']].copy()
        qual_data = qual_data[qual_data['Academic Qualification'] != 'Not Reported']
        qual_data = qual_data.sort_values('Total Total', ascending=False)
        
        fig_academic = px.bar(
            qual_data,
            x='Academic Qualification',
            y='Total Total',
            title='Teachers by Academic Qualification',
            labels={'Total Total': 'Number of Teachers', 'Academic Qualification': 'Qualification'},
            color='Total Total',
            color_continuous_scale='Teal'
        )
        fig_academic.update_traces(
            text=qual_data['Total Total'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        )
        fig_academic.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_academic, use_container_width=True)
    
    with col2:
        # Professional qualifications
        prof_total = teachers_professional[teachers_professional['Level'] == 'Total']
        prof_data = prof_total[['Professional Qualification', 'Total Total']].copy()
        prof_data = prof_data[prof_data['Professional Qualification'] != 'Not Mentioned']
        prof_data = prof_data.sort_values('Total Total', ascending=False)
        
        fig_prof = px.bar(
            prof_data,
            x='Professional Qualification',
            y='Total Total',
            title='Teachers by Professional Qualification',
            labels={'Total Total': 'Number of Teachers', 'Professional Qualification': 'Qualification'},
            color='Total Total',
            color_continuous_scale='Greens'
        )
        fig_prof.update_traces(
            text=prof_data['Total Total'].apply(lambda x: f'{x:,}'),
            textposition='outside'
        )
        fig_prof.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_prof, use_container_width=True)
    
    # Row 4: 5-Year Teacher Trends
    st.subheader("Teacher Growth Trends (2019-2024)")
    
    years = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    trend_stages = ['Primary', 'Middle', 'High', 'Higher Secondary/Inter Colleges', 'Universities']
    teacher_trends = teachers_5yr[teachers_5yr['Institution Type'].isin(trend_stages) & (teachers_5yr['Sector'] == 'Total')]
    
    fig_teacher_trend = go.Figure()
    colors = ['#0f4c3a', '#1a7f5f', '#2ea87e', '#4fd1a8', '#7ee5c7']
    
    for idx, stage in enumerate(trend_stages):
        stage_row = teacher_trends[teacher_trends['Institution Type'] == stage]
        if len(stage_row) > 0:
            values = [stage_row[year].values[0] for year in years]
            
            fig_teacher_trend.add_trace(go.Scatter(
                x=years,
                y=values,
                mode='lines+markers',
                name=stage,
                line=dict(color=colors[idx], width=3),
                marker=dict(size=8)
            ))
    
    fig_teacher_trend.update_layout(
        title='5-Year Teacher Growth Trends by Education Stage',
        xaxis_title='Academic Year',
        yaxis_title='Number of Teachers',
        height=450,
        hovermode='x unified'
    )
    st.plotly_chart(fig_teacher_trend, use_container_width=True)
    
    # Summary Statistics
    st.markdown("---")
    st.subheader("📊 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Qualification Highlights:**")
        phd_count = qual_data[qual_data['Academic Qualification'] == 'Ph.D']['Total Total'].values[0] if 'Ph.D' in qual_data['Academic Qualification'].values else 0
        ma_count = qual_data[qual_data['Academic Qualification'] == 'M.A/M.Sc']['Total Total'].values[0] if 'M.A/M.Sc' in qual_data['Academic Qualification'].values else 0
        st.write(f"• PhD Holders: {phd_count:,}")
        st.write(f"• Masters Degree: {ma_count:,}")
        st.write(f"• MPhil Holders: {qual_data[qual_data['Academic Qualification'] == 'M.Phil']['Total Total'].values[0]:,}")
    
    with col2:
        st.markdown("**Training Status:**")
        trained = prof_data[prof_data['Professional Qualification'].isin(['B.Ed/BS.Ed', 'M.Ed', 'P.T.C', 'C.T'])]['Total Total'].sum()
        untrained = prof_data[prof_data['Professional Qualification'] == 'Un-Trained']['Total Total'].values[0] if 'Un-Trained' in prof_data['Professional Qualification'].values else 0
        st.write(f"• Trained Teachers: {trained:,}")
        st.write(f"• Un-trained: {untrained:,}")
        st.write(f"• Training Rate: {(trained/(trained+untrained))*100:.1f}%")
    
    with col3:
        st.markdown("**Distribution:**")
        urban_total = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']['URBAN Total'].sum()
        rural_total = teachers_provincial[teachers_provincial['Province/Region'] == 'Pakistan']['RURAL Total'].sum()
        st.write(f"• Urban Teachers: {urban_total:,}")
        st.write(f"• Rural Teachers: {rural_total:,}")
        st.write(f"• Rural Coverage: {(rural_total/total_teachers)*100:.1f}%")
