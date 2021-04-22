import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import numpy as np

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/8b9c4569ed48bfd9c90ce851b688052120f2cc1f/us.csv", error_bad_lines=False)

app.layout = html.Div([

    html.H1("GROWTH RATE", style={'text-align': 'center'}),

       dcc.Dropdown(id="slct_state",
                 options=[
                     {"label": "Cases", "value": 'cases'},
                     {"label": "Deaths", "value": 'deaths'}],
                 multi=False,
                 value='cases',
                 style={'width': "40%"}
                 ),

        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='cases_graph', figure={})

])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='cases_graph', component_property='figure')],
    [Input(component_id='slct_state', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The value chosen by user was: {}".format(option_slctd)

    # Plotly Express
    fig = px.line(
        data_frame=df,
        x = "date",
        y = option_slctd,
        title="Growth of {}".format(option_slctd)
    )
    
    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
