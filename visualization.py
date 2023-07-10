import numpy as np
import plotly.express as px
import pandas as pd


def trips_day(combined_data):
    trip_group = combined_data.groupby(['label', 'time_range_2'])['count'].sum().reset_index()
    total_trip = trip_group['count'].sum()
    trip_group['Percentage'] = (trip_group['count'] / total_trip) * 100

    fig_trips = px.bar(
        trip_group,
        x='time_range_2',
        y='Percentage',
        color='label',
        labels={'time_range_2': 'Time of day (30 min time intervals)', 'Percentage': 'Percentage (%)', 'label': 'Scenario'},
        barmode='group',
        template='plotly',
        hover_data=['count', 'Percentage']
    )

    fig_trips.update_layout(
        title_text='Trips by Time of Day',
        title_x=0.5,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig_trips


def tours_person(combined_data):
    number_tours = combined_data.groupby(['person_id', 'label'])['count'].sum().reset_index()
    number_tours = number_tours.groupby(['count', 'label']).size().reset_index(name='Population_Count')
    number_tours['trip_count'] = pd.cut(
        number_tours['count'],
        bins=[1, 2, 3, 4, 5, float('inf')],
        labels=['1', '2', '3', '4', '+4 trips'],
        right=False
    )
    number_tours = number_tours.groupby(['label', 'trip_count'])['Population_Count'].sum().reset_index()
    category_order = ['1', '2', '3', '4', '+4 trips']
    number_tours['trip_count'] = pd.Categorical(number_tours['trip_count'], category_order)
    number_tours = number_tours.sort_values('trip_count')
    total_population = number_tours['Population_Count'].sum()
    number_tours['Percentage'] = (number_tours['Population_Count'] / total_population) * 100

    fig_tour = px.bar(
        number_tours,
        x='trip_count',
        y='Percentage',
        color='label',
        labels={'trip_count': 'Number of Tours', 'Percentage': 'Percentage (%)', 'label': 'Scenario'},
        barmode='group',
        template='plotly',
        hover_data=['Population_Count', 'Percentage']
    )

    fig_tour.update_layout(
        title_text='Number of Tours per Person',
        title_x=0.5,
        showlegend=False
    )

    return fig_tour


def mode_share(combined_data):
    mode_shares = combined_data.groupby(['label', 'mode'])['count'].sum().reset_index()
    total_mode = mode_shares['count'].sum()
    mode_shares['Percentage'] = (mode_shares['count'] / total_mode) * 100
    mode_shares = mode_shares.sort_values('count', ascending=False)

    fig_mode = px.bar(
        mode_shares,
        x='mode',
        y='Percentage',
        color='label',
        labels={'mode': 'Mode', 'Percentage': 'Percentage (%)', 'label': 'Scenario'},
        barmode='group',
        template='plotly',
        hover_data=['count', 'Percentage']
    )

    fig_mode.update_layout(
        title_text='Transport Mode Shares',
        title_x=0.5,
        showlegend=False
    )

    return fig_mode


def create_histogram_plot(combined_data, color_value):
    if color_value == 'education_category':
        distribution_education = combined_data.groupby(['label', 'education_category'])['count'].sum().reset_index()
        # Calculate the total population count
        total_education = distribution_education['label'].value_counts()
        distribution_education['Percentage'] = distribution_education.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_education = distribution_education.reset_index()
        distribution_education= distribution_education.sort_values('Percentage', ascending = True)
        fig = px.bar(distribution_education, y='education_category', x='Percentage', color='label', barmode='group',
             orientation='h',
             labels={
                 'education_category': 'Education Level',
                 'count': 'Count',
                 'label': 'Scenario',
                 'Percentage' : 'Percentage (%)'
             })
        fig.update_layout(title_text='Distribution Across Education',
                          title_x=0.5,
                          showlegend=False)
        
        
    elif color_value == 'gender':
        distribution_gender = combined_data.groupby(['label', 'gender'])['count'].sum().reset_index()
        distribution_gender['Percentage'] = distribution_gender.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_gender = distribution_gender.reset_index()
        distribution_gender= distribution_gender.sort_values('Percentage', ascending = True)
        fig = px.bar(distribution_gender, y='gender', x='Percentage', color='label', barmode='group',
             labels={
                 'gender': 'Gender',
                 'count': 'Count',
                 'label': 'Scenario',
                 'Percentage' : 'Percentage (%)'
             })
        fig.update_layout(title_text='Distribution Across Gender',
                          title_x=0.5,
                          showlegend=False)
        
    elif color_value == 'age':
        category_order_age = ['4-9yrs old', '10-14 yrs old', '15-19 yrs old', '20-24 yrs old', '25-29 yrs old',
                      '30-34 yrs old', '35-39  yrs old', '40-44 yrs old', '45-49  yrs old', '50-54 yrs old',
                      '55-59  yrs old', '60-64 yrs old', '65-69 yrs old', '70-74  yrs old', '75-79 yrs old',
                      '80-84 yrs old', '85+']
        combined_data['age'] = pd.Categorical(combined_data['age'], categories=category_order_age, ordered=True)
        distribution_age = combined_data.groupby(['label', 'age'])['count'].sum().reset_index().sort_values('age')
        distribution_age['Percentage'] = distribution_age.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_age = distribution_age.reset_index()
        fig = px.bar(distribution_age,
                     x='age',
                     y='Percentage',
                     color='label',
                     barmode='group',
                     labels={'age': 'Age',
                             'count': 'Count',
                             'label': 'Scenario',
                             'Percentage' : 'Percentage (%)'})
        
        fig.update_layout(
        title_text='Distribution Across Age',
        title_x=0.5,
        showlegend=False)
        
    elif color_value == 'range_income':
        category_order_income= ['No Income','$1-$1000','$1001-$1499','$1500-$1999','$2000-$2499','$2500-$2999','$3000-$3999','$4000-$4999',
                       '$5000-$5999','$6000-$6999','$7000-$7999','$8000 and above']
        combined_data['range_income'] = pd.Categorical(combined_data['range_income'], categories=category_order_income, ordered=True)
        distribution_income = combined_data.groupby(['label', 'range_income'])['count'].sum().reset_index().sort_values('range_income')
        distribution_income['Percentage'] = distribution_income.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_income = distribution_income.reset_index()
        fig = px.bar(distribution_income,
                     x='range_income',
                     y='Percentage',
                     color='label',
                     barmode='group',
                     labels={'range_income': 'Income Range',
                             'count': 'Count',
                             'Percentage' : 'Percentage (%)',
                             'label': 'Scenario'})
        
        fig.update_layout(
            title_text='Distribution Across Income',
            title_x=0.5,
            showlegend=False)
        
    elif color_value == 'job_name':
        distribution_job = combined_data.groupby(['label', 'job_name'])['count'].sum().reset_index()
        distribution_job['Percentage'] = distribution_job.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_job = distribution_job.reset_index()
        distribution_job= distribution_job.sort_values('Percentage', ascending = True)
        fig = px.bar(distribution_job,
                     x='Percentage',
                     y='job_name',
                     orientation='h',
                     color='label',
                     barmode='group',
                     labels={'job_name': 'Employment Status',
                             'count': 'Count',
                             'Percentage' : 'Percentage (%)',
                             'label': 'Scenario'})
        
        fig.update_layout(
            title_text='Distribution Across Employement Status',
            title_x=0.5,
            showlegend=False)
        
    return fig


def create_stacked_histogram_plot(combined_data, color_value):
    if color_value =='education_category':
        distribution_education_2 = combined_data.groupby(['label','time_range_2','education_category'])['count'].sum().reset_index()
        
        fig_2 = px.histogram(
            distribution_education_2,
            facet_col='label',
            barnorm='percent',
            title='Distribution of Trips by Education',
            x='time_range_2',
            y='count',
            color='education_category',
            nbins=20)
    elif color_value == 'gender':
        category_order_income= ['No Income','$1-$1000','$1001-$1499','$1500-$1999','$2000-$2499','$2500-$2999','$3000-$3999','$4000-$4999',
                       '$5000-$5999','$6000-$6999','$7000-$7999','$8000 and above']
        combined_data['range_income'] = pd.Categorical(combined_data['range_income'], categories=category_order_income, ordered=True)
        distribution_gender_2= combined_data.groupby(['label','time_range_2','gender'])['count'].sum().reset_index()
        fig_2 = px.histogram(
            distribution_gender_2,
            facet_col='label',
            barnorm='percent',
            title='Distribution of Trips by Gender',
            x='time_range_2',
            y='count',
            color='gender',
            nbins=20)
        
    elif color_value == 'age':
        distribution_age = combined_data.groupby(['label','time_range_2','age'])['count'].sum().reset_index()
        distribution_age['Percentage'] = distribution_age.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_age = distribution_age.reset_index()
        fig_2 = px.histogram(distribution_age,
                               facet_col='label',
                               barnorm='percent',
                               title='Distribution of Trips by Age',
                               x='time_range_2',
                               y='count',
                               color='age',
                               nbins=20)
        
    elif color_value == 'range_income':
        category_order_income= ['No Income','$1-$1000','$1001-$1499','$1500-$1999','$2000-$2499','$2500-$2999','$3000-$3999','$4000-$4999',
                       '$5000-$5999','$6000-$6999','$7000-$7999','$8000 and above']
        combined_data['range_income'] = pd.Categorical(combined_data['range_income'], categories=category_order_income, ordered=True)
        distribution_income_2 = combined_data.groupby(['label','time_range_2','range_income'])['count'].sum().reset_index()
        total_income = distribution_income_2['label'].value_counts()
        distribution_income_2['Percentage'] = distribution_income_2.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_income_2 = distribution_income_2.reset_index()
        fig_2= px.histogram(distribution_income_2,
                            facet_col='label',
                            barnorm='percent',
                            title='Distribution of Trips by Income',
                            x='time_range_2',
                            y='count',
                            color='range_income',
                            nbins=20,)
        
    elif color_value == 'job_name':
        distribution_job_2 = combined_data.groupby(['label','time_range_2','job_name'])['count'].sum().reset_index()
        total_job = distribution_job_2['label'].value_counts()
        distribution_job_2['Percentage'] = distribution_job_2.groupby('label')['count'].apply(lambda x: (x / x.sum()) * 100)
        distribution_job_2 = distribution_job_2.reset_index()
        fig_2= px.histogram(distribution_job_2,
                            facet_col='label',
                            barnorm='percent',
                            title='Distribution of Trips by Employment Status',
                            x='time_range_2',
                            y='count',
                            color='job_name',
                            nbins=20)
        
        
    return fig_2



def stacked_histogram(combined_data, color_value):
    fig_2 = px.histogram(
        combined_data,
        facet_col='label',
        title="Distribution of Trips Across Scenarios",
        x="time_range_2",
        barnorm='percent',
        color=color_value,
        nbins=10
    )
    fig_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    return fig_2
