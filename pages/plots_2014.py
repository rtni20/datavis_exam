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
monthly_avg_temp_df['date'] = monthly_avg_temp_df['date'].dt.strftime('%b %Y')

fig1 = px.scatter(df, x='date', y='actualMeanTemp',
                  labels={'date': 'Date', 'actualMeanTemp': 'Temperature (f)'},
                  title="The average temperature on daily basis",
                  color_discrete_sequence=['#00BFFF'])
fig2 = px.bar(monthly_avg_temp_df, x='date', y='actualMeanTemp',
              labels={'date': 'Date', 'actualMeanTemp': 'Average Temperature (f)'},
              title='The average temperature on monthly basis',
              color_discrete_sequence=['#00BFFF'])


layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on temperatures from 2014-2015'),
    dcc.Link('Go back to main menu', href='/'),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link('Go back to previous page', href='/guide_and_introduction'), width='auto'),
            dbc.Col(dcc.Link('Go to next page', href='/plots_min_max'), width='auto')], justify='between')
    ]),
    html.Div([
        dbc.Col([
            html.H6('What is the highest and lowest temperature measured in 2014/2015?'),
            dcc.Graph(figure=fig1),
            html.H6('Which month(s) has the average highest and lowest temperature?'),
            dcc.Graph(figure=fig2)
        ], width=8)
    ]),
    html.Div(id='2014_plots_page')
])
