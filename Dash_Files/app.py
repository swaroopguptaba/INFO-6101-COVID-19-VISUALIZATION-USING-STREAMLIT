import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
from graphs import display_choropleth


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# init the app and server
app = dash.Dash()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[

    html.Div(children=[
        dcc.RadioItems(
            id='select_category',
            className='radio-group',
            options=[{"label": "Total Cases", "value": 'cases'},
                     {"label": "Total Deaths", "value": 'deaths'}],
            value='cases',
            labelStyle={'display': 'inline-block'}
        ),

        dcc.Graph(id="choropleth"),

    ], className="row"),
], className="container-fluid")


@app.callback(
    Output("choropleth", "figure"),
    Input('select_category', 'value'))
def update_choropleth(select_category):
    return display_choropleth(select_category)


app.run_server(debug=True)
