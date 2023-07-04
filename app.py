import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
import geopandas as gpd
from keplergl import KeplerGl

from dash import dcc
from dash import html


from data_processing import process_files

from visualization import create_histogram_plot

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("SimMobility", className="display-4"),
        html.Hr(),
        html.P(
            "Welcome to the SimMobility Subtrip dashboard, please upload your files below in order to view your simulation data",
            className="lead"
        )
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        html.H2("Drop your Subtrip.csv files below", className="display-5"),
        html.P("This is the text container where you can put your text."),
        # Additional text components or layout can be added here
        dcc.Upload(
            [
                'Drag and Drop or ',
                html.A('Select a File')
            ],
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            },
            id='upload-data',
            multiple=True
        ),
        html.Div(id='file-list'),  # Added the file-list component here
        html.Button('Process Files', id='transform-button', n_clicks=0),
        html.Hr(),
        dcc.Loading(
            id='loading',
            type='default',
            children=[
                html.Div(
                    [
                        dcc.Dropdown(
                            id='color-dropdown',
                            options=
                            [
                                {'label':'Education','value':'education_category'},
                                {'label':'Income','value':'range_income'},
                                {'label':'Gender','value':'gender'},
                                {'label':'Age','value':'age'},
                                {'label':'Transport Mode','value':'mode'},
                                {'label':'Trip Count','value':'distr'},
                            ],
                            value='distr',
                            clearable= False,
                            style={'display': 'none'}
                        )
                    ]
                ),
                html.Div(id='visualization-1', style={'display': 'none'}),
                html.Iframe(id='map-iframe', height='1000', width='1000', src='', style={'display': 'none'})
                
            ],
        ),
        html.Div(id='alert-message'),  # Added the alert message div
    ],
    id="page-content",
    style=CONTENT_STYLE
)

@app.callback(
    [
        Output('visualization-1', 'children'),
        Output('visualization-1', 'style'),
        Output('color-dropdown', 'style'), 
        Output('alert-message', 'children'),
        Output('map-iframe', 'src') 
    ],
    [
        Input('transform-button', 'n_clicks'),
        Input('color-dropdown', 'value')  # Add this line to get the dropdown value
    ],
    [State('upload-data', 'contents')],
    prevent_initial_call=True
)
def process_uploaded_files(n_clicks,color_value, contents):
    if contents is None or len(contents) == 0:
        return [], {'display': 'none'}, html.Div('Please upload files before processing.')
    else:
        combined_data = process_files(contents)

        if combined_data is not None:
            
            fig =create_histogram_plot(combined_data, color_value)
            
            zones = gpd.read_file('data/shp_files/sm_zone.shp')
            zones.to_crs(epsg=4326)
            
            combined_data['start_time'] = combined_data['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S') 
            combined_data['time_range'] = combined_data['time_range'].dt.strftime('%Y-%m-%d %H:%M:%S') 
            
            
            config = {}
            exec(open("kepler_config.py").read(), config)
            config = config["config"]
            map_1 = KeplerGl(height=800, data={'zones': zones, 'trips': combined_data}, config=config)
            map_1.save_to_html(file_name="map_kepler.html")

            with open('map_kepler.html', 'r') as f:
                kepler_html = f.read()
            
            
            return (
                dcc.Graph(figure=fig),
                {'display': 'block'},
                {'display': 'block'},
                html.Iframe(srcDoc=kepler_html, height='1000', width='1000'),
                'map_kepler.html'
            )
        else:
            return [], {'display': 'none'}, html.Div('No file uploaded yet.'), '',



@app.callback(
    Output('file-list', 'children'),
    [Input('upload-data', 'filename')],
    prevent_initial_call=True
)
def update_file_list(filenames):
    if filenames:
        return html.Ul([
            html.Li(filename) for filename in filenames
        ])
    else:
        return html.Div('No files selected.')


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)
