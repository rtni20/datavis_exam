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
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

actual_precipitation_df = df[['date', 'actualPrecipitation']].copy()
actual_precipitation_mean = actual_precipitation_df.groupby(pd.Grouper(key='date', freq='M')).mean()
actual_precipitation_mean.reset_index(inplace=True)
actual_precipitation_mean.rename(columns={'date': 'month', 'actualPrecipitation': 'monthlyAverageActualPrecipitation'}, inplace=True)

mean_precipitation_df = df[['date', 'averagePrecipitation']].copy()
mean_precipitation = mean_precipitation_df.groupby(pd.Grouper(key='date', freq='M')).mean()
mean_precipitation.reset_index(inplace=True)
mean_precipitation.rename(columns={'date': 'month', 'averagePrecipitation': 'monthlyAveragePrecipitation'}, inplace=True)

final_df = pd.merge(actual_precipitation_mean, mean_precipitation, how='outer', on=['month'])

fig1 = go.Figure(data=[
    go.Bar(name='Monthly average 2014-2015', x=final_df['month'], y=final_df['monthlyAverageActualPrecipitation']),
    go.Bar(name='Monthly average since 1880', x=final_df['month'], y=final_df['monthlyAveragePrecipitation'])
])
fig1.update_layout(barmode='group', yaxis_title='Precipitation amount', xaxis_title='Date')

layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on weather data from 2014-2015 and average precipitation from 1880'),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig1)
            ], width=8)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='daily_precipitation_plot')
            ], width=8),
            dbc.Col([
                dcc.Graph(id='precipitation_barchart')
            ], width=4)
        ])
    ]),
    html.Div(id='rain_snow_page'),
    dcc.Link('Go to next plot', href='/plot_record_year'),
    html.Br(),
    dcc.Link('Go back to main menu', href='/')
])

@app.callback(
    Output(component_id='daily_precipitation_plot', component_property='figure'),
    Input(component_id='daily_precipitation_plot', component_property='clickdata')
)
def update_daily_plot(clickdata):
    if clickdata is not None:
        clicked_date = clickdata['points'][0]['customdata'][0]
        for index, date in enumerate(df['date']):
            if clicked_date == date:
                df.at[index, 'selected'] = not df.at[index, 'selected']
                print(df)

        fig = px.line(df, x='date', y='actualPrecipitation', markers=True,
                      custom_data=['date', 'actualPrecipitation', 'averagePrecipitation', 'recordPrecipitation'])
        return fig

    else:
        fig = px.line(df, x='date', y='actualPrecipitation', markers=True,
                      custom_data=['date', 'actualPrecipitation', 'averagePrecipitation', 'recordPrecipitation'])
        return fig





