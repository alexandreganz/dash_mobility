import numpy as np
import plotly.express as px
import pandas as pd




def trips_day(combined_data):
    trip_group =  combined_data.groupby(['label','time_range'])['count'].sum().reset_index()
    # Calculate the total population count
    total_trip = trip_group['count'].sum()

    # Add a percentage column
    trip_group['Percentage'] = (trip_group['count'] / total_trip) * 100


    # Create a bar plot using Plotly
    fig_trips = px.bar(trip_group, x='time_range', y='Percentage', color='label',
                labels={'time_range': 'Time of day (30 min time intervals)', 'Percentage': 'Percentage (%)', 'label':'Scenario'},
                barmode='group',
                title='Trips by Time of Day',
                template='plotly',
                hover_data=['count', 'Percentage'])


    fig_trips.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig_trips


def tours_person(combined_data):
    # Group by 'person_id' and 'label', and sum the 'count' column
    number_tours = combined_data.groupby(['person_id', 'label'])['count'].sum().reset_index()

    # Group by 'count' and 'label', and count the occurrences
    number_tours = number_tours.groupby(['count', 'label']).size().reset_index(name='Population_Count')

    # Replace values greater than 4 with '+4 trips' in a new column 'trip_count'
    number_tours['trip_count'] = pd.cut(number_tours['count'], bins=[1, 2, 3, 4, 5,float('inf')],
                                    labels=['1', '2', '3', '4', '+4 trips'], right=False)

    # Group by 'label' and 'trip_count', and sum the 'Population_Count' column
    number_tours = number_tours.groupby(['label', 'trip_count'])['Population_Count'].sum().reset_index()

    # Define the order of the 'trip_count' categories
    category_order = ['1', '2', '3', '4', '+4 trips']

    # Convert 'trip_count' to categorical with the defined order
    number_tours['trip_count'] = pd.Categorical(number_tours['trip_count'], category_order)

    # Sort the DataFrame based on the categorical order
    number_tours = number_tours.sort_values('trip_count')

    # Calculate the total population count
    total_population = number_tours['Population_Count'].sum()

    # Add a percentage column
    number_tours['Percentage'] = (number_tours['Population_Count'] / total_population) * 100
    
        # Create a bar plot using Plotly
    fig_tour = px.bar(number_tours, x='trip_count', y='Percentage', color='label',
                labels={'trip_count': 'Number of Tours', 'Percentage': 'Percentage (%)', 'label':'Scenario'},
                barmode='group',
                title='Number of Tours per Person',
                template='plotly',
                hover_data=['Population_Count', 'Percentage'])


    fig_tour.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    return fig_tour


















def create_histogram_plot(combined_data, color_value):
    if color_value == 'education_category':
        education_group = combined_data.groupby(['label', 'start_time', 'education_category'])['count'].sum().reset_index()
        fig = px.histogram(education_group,
                           facet_col='label',
                           title='Distribution of Trips by Education',
                           x='start_time',
                           y='count',
                           color='education_category',
                           )
    elif color_value == 'range_income':
        income_group = combined_data.groupby(['label', 'start_time', 'range_income'])['count'].sum().reset_index()
        fig = px.histogram(income_group,
                           facet_col='label',
                           title='Distribution of Trips by Education',
                           x='start_time',
                           y='count',
                           color='range_income',
                           )

    fig.update_layout(height=600) 

    return fig




def stacked_histogram(combined_data, color_value):
    fig_2 = px.histogram(combined_data, 
                   facet_col='label',
                   title="Distribution of Trips Across Scenarios",
                   x="time_range",
                   barnorm ='percent',
                   color=color_value,
                   nbins=10)
    fig_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    
    return fig_2
    
    
    
    

