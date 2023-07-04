import numpy as np
import plotly.express as px
import pandas as pd

def create_histogram_plot(combined_data, color_value):
    
    
    
    x_max = np.max(combined_data['time_range'])
            
    fig = px.histogram(combined_data, 
                       facet_col='label',
                       title="Distribution of Trips Across Scenarios",
                       x="time_range", 
                       color=color_value,
                       marginal="box",
                       nbins=20)
            
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            
    fig.update_layout(height=600) 

    # Check if the maximum value of x-axis data is greater than the threshold
    if x_max >= pd.Timestamp("1900-01-01 09:30:00"):
        fig.add_vrect(x0="1900-01-01 07:30:00", x1="1900-01-01 09:30:00",
                      annotation_text="Morning Peak",
                      fillcolor="red", opacity=0.25, line_width=0)

    if x_max >= pd.Timestamp("1900-01-01 14:00:00"):
        fig.add_vrect(x0="1900-01-01 11:00:00", x1="1900-01-01 14:00:00",
                      annotation_text="Off Peak",
                      fillcolor="green", opacity=0.25, line_width=0)

    if x_max >= pd.Timestamp("1900-01-01 18:30:00"):
        fig.add_vrect(x0="1900-01-01 17:00:00", x1="1900-01-01 18:30:00",
                      annotation_text="Evening Peak",
                      fillcolor="orange", opacity=0.25, line_width=0)
    
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
    
    
    
    

