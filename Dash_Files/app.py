import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
from graphs import display_choropleth, growth_cases_graph, state_wise_timeseries
from data import get_unique_states


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df1 = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/bc60b7c7cefbc17a4e3fe6c3a6e86c65f88ca91d/us-states.csv", error_bad_lines=False)


# init the app and server
app = dash.Dash()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.Br(),
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
    html.Br(),
    html.Div([  # USA-growth/cases
        dcc.Dropdown(id="slct_type",
                     options=[
                         {"label": "Cases", "value": 'cases'},
                         {"label": "Deaths", "value": 'deaths'}],
                     multi=False,
                     value='cases'
                     ),

        html.Div(id='output_container1', children=[]),
        #dcc.Graph(id='cases_graph', figure={}, style={'width': '50%', 'height': '30%'})
        dcc.Graph(id='cases_graph', figure={})

    ],
        style={'display': 'inline-block', 'width': '50%'}),


    # html.Br(),
    html.Div([  # state-wise
        html.H5("StateWise", "margin-left: 45%"),
        dcc.Dropdown(id="slct_state",
                     options=[{'value': x, 'label': x}
                              for x in get_unique_states()],
                     multi=False,
                     value='Alabama',
                     style={'width': "40%"}
                     ),
        dcc.Dropdown(id="slct_new",
                     options=[
                         {"label": "Cases", "value": 'cases'},
                         {"label": "Deaths", "value": 'deaths'}],
                     multi=False,
                     value='cases',
                     ),

        html.Div(id='output_container2', children=[]),
        html.Br(),

        dcc.Graph(id='state_graph', figure={})

    ],
        style={'display': 'inline-block', 'width': '50%'}
    )


], className="container-fluid")


@app.callback(
    Output("choropleth", "figure"),
    Input('select_category', 'value'))
def update_choropleth(select_category):
    return display_choropleth(select_category)


@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='cases_graph', component_property='figure')
     ],
    [Input(component_id='slct_type', component_property='value')]
)
def update_cases_graph(slct_type):
    return growth_cases_graph(slct_type)


@app.callback(
    [Output(component_id='output_container2', component_property='children'),
        Output('state_graph', 'figure')],
    [Input('slct_state', 'value'),
     Input('slct_new', 'value')]
)
def update_graph(slct_state, slct_new):
    return state_wise_timeseries(slct_state, slct_new)


app.run_server(debug=True)
