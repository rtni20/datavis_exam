import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data_frame_function import get_weather_data

df = get_weather_data()
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

monthly_average_temp = df.groupby(pd.PeriodIndex(df['date'], freq="m"))['actualMeanTemp'].mean()
monthly_average_temp.reset_index()
print(monthly_average_temp)


fig1 = px.scatter(df, x='date', y='actualMeanTemp', labels={'date': 'Date', 'actualMeanTemp': 'Temperature (f)'})



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
