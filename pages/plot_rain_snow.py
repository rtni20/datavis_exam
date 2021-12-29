import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from data_frame_function import get_weather_data

df = get_weather_data()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

actual_precipitation_df = df[['date', 'actualPrecipitation']].copy()
actual_precipitation_mean = actual_precipitation_df.groupby(pd.Grouper(key='date', freq='M')).mean()
actual_precipitation_mean.reset_index(inplace=True)

mean_precipitation_df = df[['date', 'averagePrecipitation']].copy()
mean_precipitation = mean_precipitation_df.groupby(pd.Grouper(key='date', freq='M')).mean()
mean_precipitation.reset_index(inplace=True)

final_df = pd.merge(actual_precipitation_mean, mean_precipitation, how='outer', on=['date'])


fig1 = go.Figure(data=[
    go.Bar(name='Monthly average 2014-2015', x=final_df['date'], y=final_df['actualPrecipitation']),
    go.Bar(name='Monthly average since 1880', x=final_df['date'], y=final_df['averagePrecipitation'])
])
fig1.update_layout(barmode='group')

layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on weather data from 2014-2015 and average precipitation from 1880'),
    html.Div([
        dbc.Col([
            dcc.Graph(figure=fig1)
        ], width=8)
    ]),
    html.Div(id='rain_snow_page'),
    dcc.Link('Go to next plot', href='/guide_and_introduction'),
    html.Br(),
    dcc.Link('Go back to main menu', href='/')
])