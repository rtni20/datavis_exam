import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from data_frame_function import get_weather_data

df = get_weather_data()

df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
monthly_avg_temp_df = df.groupby(pd.Grouper(key='date', freq='M')).mean()
monthly_avg_temp_df.reset_index(inplace=True)
#monthly_avg_temp_df['date'] = monthly_avg_temp_df['date'].dt.to_period('M')
monthly_avg_temp_df['date'] = monthly_avg_temp_df['date'].dt.strftime('%b %Y')

fig1 = px.scatter(df, x='date', y='actualMeanTemp', labels={'date': 'Date', 'actualMeanTemp': 'Temperature (f)'})
fig2 = px.bar(monthly_avg_temp_df, x='date', y='actualMeanTemp',
              labels={'date': 'Date', 'actualMeanTemp': 'Average Temperature (f)'})


layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on weather data from 2014-2015'),
    html.Div([
        dbc.Col([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ], width=8)
    ]),
    html.Div(id='2014_plots_page'),
    dcc.Link('Go to next plot', href='/plots_min_max'),
    html.Br(),
    dcc.Link('Go back to main menu', href='/')
])
