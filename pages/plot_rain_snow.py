import dash
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
final_df['month'] = final_df['month'].dt.strftime('%b %Y')

#This is for the alternative plot
actual_total = final_df['monthlyAverageActualPrecipitation'].sum()
average_total = final_df['monthlyAveragePrecipitation'].sum()
labels = ['Monthly average 2014-2015', 'Monthly average since 1880']
values = [actual_total, average_total]
colors = ['#00BFFF', '#FFD700']

fig1 = go.Figure()
fig1.add_trace(go.Bar(name='Monthly average 2014-2015',
                      x=final_df['month'],
                      y=final_df['monthlyAverageActualPrecipitation'],
                      marker_color='#00BFFF'))
fig1.add_trace(go.Bar(name='Monthly average since 1880',
                      x=final_df['month'],
                      y=final_df['monthlyAveragePrecipitation'],
                      marker_color='#FFD700'))

fig1.update_layout(barmode='group', yaxis_title='Precipitation amount (in)', xaxis_title='Date',
                   title_text='Average precipitation on monthly basis')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['date'], y=df['actualPrecipitation'],
                          mode='markers',
                          marker_color='#00BFFF'))
fig2.update_layout(yaxis=dict(tick0=0, dtick=0.1), yaxis_title='Precipitation amount (in)', xaxis_title='Date',
                   title_text='Actual Precipitation on daily basis')

#alternative plot
fig3 = go.Figure()
fig3.add_trace(go.Pie(labels=labels, values=values, hole=.3))
fig3.update_traces(marker=dict(colors=colors))


layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Plots based on precipitation from 2014-2015 and average precipitation since 1880'),
    dcc.Link('Go back to main menu', href='/'),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link('Go back to previous page', href='/plots_min_max'), width='auto'),
            dbc.Col(dcc.Link('Go to next page', href='/plot_record_year'), width='auto')], justify='between')
    ]),
    html.Div([
        dbc.Row([
            html.H6('Is the monthly average of precipitation in 2014/2015 in general greater or lower compared to the average measurement since 1880?'),
            dbc.Col([
                dcc.Graph(figure=fig1)
            ], width=8),
            dbc.Col([
                dcc.Graph(figure=fig3)
            ], width=4)
        ]),
        dbc.Row([
            html.H5('Move the cursor over the visualisation to make the plot on the right side appear!'),
            html.H6('How many days in 2014/2015 did the actual precipitation match the record measurement?'),
            dbc.Col([
                dcc.Graph(figure=fig2, id='precipitation_scatter_plot', style={'height': '70vh'})
            ], width=7),
            dbc.Col([
                dcc.Graph(id='multiple_cat_bar', style={'height': '70vh'})
            ], width=5)
        ])
    ]),
    html.Div(id='rain_snow_page')
])


@app.callback(Output("multiple_cat_bar", "figure"),
              [Input("precipitation_scatter_plot", "hoverData")])
def on_hover(hover_data):
    if not hover_data:
        return dash.no_update

    date = hover_data["points"][0]["x"]

    precipitation = df.loc[df['date'] == date]
    columns = ['Precipitation']

    multibar = go.Figure()
    multibar.add_trace(go.Bar(x=columns, y=precipitation.actualPrecipitation,
                              name='Actual Precipitation',
                              marker_color='#00BFFF'))
    multibar.add_trace(go.Bar(x=columns, y=precipitation.averagePrecipitation,
                              name='Average Precipitation',
                              marker_color='#228B22'))
    multibar.add_trace(go.Bar(x=columns, y=precipitation.recordPrecipitation,
                              name='Record Precipitation',
                              marker_color='#FFD700'))
    multibar.update_layout(barmode='group', yaxis_title='Amount (in)', xaxis_title='Precipitation',
                           title_text='Actual-, Average- and Record precipitation for a selected date')
    multibar.update_layout(yaxis_range=[0, 8.5])
    return multibar






