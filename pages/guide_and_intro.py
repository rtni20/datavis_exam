import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H1('Weather data from New York City'),
    html.H3('Introduction and Guide'),
    dcc.Link('Go back to main menu', href='/'),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link('Go back to previous page', href='/plot_record_year'), width='auto'),
            dbc.Col(dcc.Link('Go to next page', href='/plots_2014'), width='auto')], justify='between')
    ]),
    html.H6('''The intention of this page is to give an introduction. 
    The data is collected from WU (Weather Underground) and contains data regarding the weather in New York City. 
    The data set contains variables for a measurement of the temperatures and precipitation for each day from the 1 July 2014 until 30 June 2015. 
    Furthermore, it contains the average measurement of each date since 1880. Due to global warming, it could be interesting to investigate if this factor affected the measurements.
    Each page contains one or several plots. It is possible to enter the next page above, but it is also possible to return to the main menu and choose a page.
    Each page contains one or multiple question, which can be answered by examining the plots in the page. 
    When the questions in one page is answered, it is possible to move on to the next page by clicking on it.'''),
    html.Div(id='intro_and_guide_page')
])
