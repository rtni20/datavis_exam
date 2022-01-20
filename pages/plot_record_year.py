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
    html.H3('Plots based on temperature record measurements'),
    dcc.Link('Go back to main menu', href='/'),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link('Go back to previous page', href='/plot_rain_snow'), width='auto'),
            dbc.Col(dcc.Link('Go to guide and introduction', href='/guide_and_introduction'), width='auto')], justify='between')
    ]),
    html.Div([
        dcc.Dropdown(id='trendlines_dropdown',
                     options=[
                         {'label': 'None', 'value': 'none'},
                         {'label': 'Temperature linear trend line', 'value': 'linear'},
                         {'label': 'Temperature logarithmic trend line', 'value': 'log'}
                     ], value='none'),
        dbc.Col([
            html.H6('Which year has the most minimum records? And which year has the most maximum record?'),
            html.H6('Does the trend lines indicate that global warming has an impact on the temperatures?'),
            dcc.Graph(id='bubble_chart', style={'height': '70vh'})
        ], width=8)
    ]),
    html.Div(id='2014_plots_page'),
])


@app.callback(Output("bubble_chart", "figure"),
              [Input("trendlines_dropdown", "value")])
def update_trendlines(value):
    if value == 'none':
        fig = px.scatter(final_df, x='year', y='freq', size='freq', color='type',
                         color_discrete_sequence=['#00BFFF', '#228B22'])
        fig.update_layout(title='Record measurements for minimum and maximum temperatures',
                          xaxis_title='Year',
                          yaxis_title='Frequency')
        return fig

    elif value == 'linear':
        fig = px.scatter(final_df, x='year', y='freq', size='freq', color='type', trendline='ols',
                         color_discrete_sequence=['#00BFFF', '#228B22'])
        fig.update_layout(title='Record measurements for minimum and maximum temperatures',
                          xaxis_title='Year',
                          yaxis_title='Frequency')
        return fig

    else:
        fig = px.scatter(final_df, x='year', y='freq', size='freq', color='type',
                         trendline="ols", trendline_options=dict(log_x=True),
                         color_discrete_sequence=['#00BFFF', '#228B22'])
        fig.update_layout(title='Record measurements for minimum and maximum temperatures',
                          xaxis_title='Year',
                          yaxis_title='Frequency')
        return fig


