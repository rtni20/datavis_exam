import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np
from data_frame_function import get_weather_data

df = get_weather_data()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on weather data from 2014-2015 and average weather data from 1880'),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='min_plot')
            ], width=8),
            dbc.Col([
                dcc.Checklist(id='show_avg_min', options=[{'label': 'Show average minimum temperature', 'value': 'YES'}],
                              value=[])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='max_plot')
            ], width=8),
            dbc.Col([dcc.Checklist(id='show_avg_max', options=[{'label': 'Show average maximum temperature', 'value': 'YES'}],
                                   value=[])
            ])
        ])
    ]),
    html.Div(id='plots_min_max_pages'),
    dcc.Link('Go to next plot', href='/plot_rain_snow'),
    html.Br(),
    dcc.Link('Go back to main menu', href='/')
])

@app.callback(
    Output(component_id='min_plot', component_property='figure'),
    Input(component_id='show_avg_min', component_property='value')
)
def update_min_plot(value):
    if len(value) == 0:
        min_plot = go.Figure(data=[
            go.Scatter(name='Actual minimum temperature 2014-2015', x=df['date'], y=df['actualMinTemp'], mode='lines',
                       legendrank=1)
        ])
        return min_plot

    else:
        min_plot = go.Figure(data=[
            go.Scatter(name='Actual minimum temperature 2014-2015', x=df['date'], y=df['actualMinTemp'],
                       mode='lines',
                       legendrank=1)
        ])
        min_plot.add_trace(go.Scatter(x=df['date'], y=df['averageMinTemp'],
                                      mode='lines',
                                      name='Average minimum temperature since 1880',
                                      legendrank=2))
        return min_plot


@app.callback(
    Output(component_id='max_plot', component_property='figure'),
    Input(component_id='show_avg_max', component_property='value')
)
def update_max_plot(value):
    if len(value) == 0:
        max_plot = go.Figure(data=[
            go.Scatter(name='Actual maximum temperature 2014-2015', x=df['date'], y=df['actualMaxTemp'], mode='lines',
                       legendrank=1)
        ])
        return max_plot

    else:
        max_plot = go.Figure(data=[
            go.Scatter(name='Actual maximum temperature 2014-2015', x=df['date'], y=df['actualMaxTemp'],
                       mode='lines',
                       legendrank=1)
        ])
        max_plot.add_trace(go.Scatter(x=df['date'], y=df['averageMaxTemp'],
                                      mode='lines',
                                      name='Average maximum temperature since 1880',
                                      legendrank=2))
        return max_plot
