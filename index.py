import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from pages import guide_and_intro, plots_2014, plots_min_max, plot_rain_snow

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H1('Weather data from New York City'),
    html.H5('This program will investigate and make statistical analysis on data regarding the weather i New York City.'),
    html.H6('Select "Guide and introduction" to get started. Otherwise, select a arbitrary page to make plots appear.'),
    dcc.Link('Guide and introduction', href='/guide_and_introduction'),
    html.Br(),
    dcc.Link('2014-2015 plots', href='/plots_2014'),
    html.Br(),
    dcc.Link('Minimum- and maximum temperatures', href='/plots_min_max'),
    html.Br(),
    dcc.Link('Precipitation', href='/plot_rain_snow')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/guide_and_introduction':
        return guide_and_intro.layout
    elif pathname == '/plots_2014':
        return plots_2014.layout
    elif pathname == '/plots_min_max':
        return plots_min_max.layout
    elif pathname == '/plot_rain_snow':
        return plot_rain_snow.layout
    else:
        return layout_index


if __name__ == '__main__':
    app.run_server(debug=True)

