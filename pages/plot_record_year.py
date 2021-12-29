import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import pandas as pd
import numpy as np
from data_frame_function import get_weather_data

df = get_weather_data()

df_max_temp_year = df[['recordMaxTempYear']].copy()
df_max_temp_year['freq'] = df.groupby('recordMaxTempYear')['recordMaxTempYear'].transform('count')
df_max_temp_year['type'] = 'max'
df_max_temp_year.rename(columns={'recordMaxTempYear': 'year'}, inplace=True)
df_max_temp_year.drop_duplicates(subset=['year'], inplace=True)

df_min_temp_year = df[['recordMinTempYear']].copy()
df_min_temp_year['freq'] = df.groupby('recordMinTempYear')['recordMinTempYear'].transform('count')
df_min_temp_year['type'] = 'min'
df_min_temp_year.rename(columns={'recordMinTempYear': 'year'}, inplace=True)
df_min_temp_year.drop_duplicates(subset=['year'], inplace=True)

final_df = df_max_temp_year.append(df_min_temp_year)


fig1 = px.scatter(final_df, x='year', y='freq', size='freq', color='type', trendline="ols")
layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on weather data from 2014-2015'),
    html.Div([
        dbc.Col([
            dcc.Graph(figure=fig1)
        ], width=8)
    ]),
    html.Div(id='2014_plots_page'),
    dcc.Link('Go to next plot', href='/guide_and_introduction'),
    html.Br(),
    dcc.Link('Go back to main menu', href='/')
])