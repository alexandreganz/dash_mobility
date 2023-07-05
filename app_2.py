"""
This app creates an animated sidebar using the dbc.Nav component and some local
CSS. Each menu item has an icon, when the sidebar is collapsed the labels
disappear and only the icons remain. Visit www.fontawesome.com to find
alternative icons to suit your needs!

dcc.Location is used to track the current location, a callback uses the current
location to render the appropriate page content. The active prop of each
NavLink is set automatically according to the current pathname. To use this
feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
import geopandas as gpd
from keplergl import KeplerGl

from data_processing import process_files

from visualization import create_histogram_plot


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("Sidebar"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Virtual City")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Boston"),
                    ],
                    href="/calendar",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-envelope-open-text me-2"),
                        html.Span("Singapoore"),
                    ],
                    href="/messages",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)




content = html.Div(id="page-content", className="content")


vc_content = html.Div(
            [
                html.H2("Drop your Subtrip.csv files below", className="display-5"),
                html.P("This is the text container where you can put your text."),
                
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
                    multiple=True),
                html.Div(id='file-list'),
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
                                    options=[
                                        {'label': 'Education', 'value': 'education_category'},
                                        {'label': 'Income', 'value': 'range_income'},
                                        {'label': 'Gender', 'value': 'gender'},
                                        {'label': 'Age', 'value': 'age'},
                                        {'label': 'Transport Mode', 'value': 'mode'},
                                        {'label': 'Trip Count', 'value': 'distr'},
                                        ],
                                    value='distr',
                                    clearable=False,
                                    style={'display': 'none'}
                                    )
                                ]
                            ),
                        dbc.Row(html.Div(id='visualization-1', style={'display': 'none'})),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                ]
                            ),
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                ]
                            )
                        ],
                    ),
                html.Div(id='alert-message'),
                ],
            id="page-content",className="vc-content"

            )


vc_conten_2 = html.Div(
            [
                html.H2("Drop your Subtrip.csv files below", className="display-5"),
                html.P("This is the text container where you can put your text."),
                
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
                    multiple=True),
                html.Div(id='file-list'),
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
                                    options=[
                                        {'label': 'Education', 'value': 'education_category'},
                                        {'label': 'Income', 'value': 'range_income'},
                                        {'label': 'Gender', 'value': 'gender'},
                                        {'label': 'Age', 'value': 'age'},
                                        {'label': 'Transport Mode', 'value': 'mode'},
                                        {'label': 'Trip Count', 'value': 'distr'},
                                        ],
                                    value='distr',
                                    clearable=False,
                                    style={'display': 'none'}
                                    )
                                ]
                            ),
                        dbc.Row(html.Div(id='visualization-1', style={'display': 'none'})),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                ]
                            ),
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(dbc.Col(html.Div("A single column"))),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                dbc.Col(html.Div("One of three columns")),
                                ]
                            )
                        ],
                    ),
                html.Div(id='alert-message'),
                ],
            id="page-content",className="vc-content"

            )





@app.callback(
    [
        Output('visualization-1', 'children'),
        Output('visualization-1', 'style'),
        Output('color-dropdown', 'style'), 
        Output('alert-message', 'children'),
    ],
    [
        Input('transform-button', 'n_clicks'),
        Input('color-dropdown', 'value')  # Add this line to get the dropdown value
    ],
    [State('upload-data', 'contents')],
    prevent_initial_call=True
)
def process_uploaded_files(n_clicks, color_value, contents):
    if contents is None or len(contents) == 0:
        return [], {'display': 'none'}, {'display': 'none'}, html.Div('Please upload files before processing.')
    else:
        combined_data = process_files(contents)

        if combined_data is not None:
            fig = create_histogram_plot(combined_data, color_value)
            return [
                dcc.Graph(figure=fig),
                {'display': 'block'},
                {'display': 'block'},
                ''
            ]
        else:
            return [], {'display': 'none'}, {'display': 'none'}, html.Div('No file uploaded yet.')


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


# set the content according to the current pathname
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return vc_content
    elif pathname == "/calendar":
        return vc_conten_2
    elif pathname == "/messages":
        return html.P("Here are all your messages")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)