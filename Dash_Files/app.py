import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
from graphs import display_choropleth


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/8b9c4569ed48bfd9c90ce851b688052120f2cc1f/us.csv", error_bad_lines=False)
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


    #html.Br(),
    html.Div([  # state-wise
        html.H5("StateWise", "margin-left: 45%"),
        dcc.Dropdown(id="slct_state",
                     options=[
                         {"label": "Alabama", "value": 'Alabama'},
                         {"label": "Alaska", "value": "Alaska"},
                         {"label": "Arizona", "value": "Arizona"},
                         {"label": "Arkansas", "value": "Arkansas"},
                         {"label": "California", "value": "California"},
                         {"label": "Colorado", "value": "Colorado"},
                         {"label": "Connecticut", "value": "Connecticut"},
                         {"label": "Delaware", "value": "Delaware"},
                         {"label": "District of Columbia",
                          "value": "District of Columbia"},
                         {"label": "Florida", "value": "Florida"},
                         {"label": "Georgia", "value": "Georgia"},
                         {"label": "Guam", "value": "Guam"},
                         {"label": "Hawaii", "value": "Hawaii"},
                         {"label": "Idaho", "value": "Idaho"},
                         {"label": "Illinois", "value": "Illinois"},
                         {"label": "Indiana", "value": "Indiana"},
                         {"label": "Iowa", "value": "Iowa"},
                         {"label": "Kansas", "value": "Kansas"},
                         {"label": "Kentucky", "value": "Kentucky"},
                         {"label": "Louisiana", "value": "Louisiana"},
                         {"label": "Maine", "value": "Maine"},
                         {"label": "Maryland", "value": "Maryland"},
                         {"label": "Massachusetts", "value": "Massachusetts"},
                         {"label": "Michigan", "value": "Michigan"},
                         {"label": "Minnesota", "value": "Minnesota"},
                         {"label": "Mississippi", "value": "Mississippi"},
                         {"label": "Missouri", "value": "Missouri"},
                         {"label": "Montana", "value": "Montana"},
                         {"label": "Nebraska", "value": "Nebraska"},
                         {"label": "Nevada", "value": "Nevada"},
                         {"label": "New Hampshire", "value": "New Hampshire"},
                         {"label": "New Jersey", "value": "New Jersey"},
                         {"label": "New Mexico", "value": "New Mexico"},
                         {"label": "New York", "value": "New York"},
                         {"label": "North Carolina", "value": "North Carolina"},
                         {"label": "North Dakota", "value": "North Dakota"},
                         {"label": "Northern Mariana Islands",
                          "value": "Northern Mariana Islands"},
                         {"label": "Ohio", "value": "Ohio"},
                         {"label": "Oklahoma", "value": "Oklahoma"},
                         {"label": "Oregon", "value": "Oregon"},
                         {"label": "Pennsylvania", "value": "Pennsylvania"},
                         {"label": "Puerto Rico", "value": "Puerto Rico"},
                         {"label": "Rhode Island", "value": "Rhode Island"},
                         {"label": "South Carolina", "value": "South Carolina"},
                         {"label": "South Dakota", "value": "South Dakota"},
                         {"label": "Tennessee", "value": "Tennessee"},
                         {"label": "Texas", "value": "Texas"},
                         {"label": "Utah", "value": "Utah"},
                         {"label": "Vermont", "value": "Vermont"},
                         {"label": "Virgin Islands", "value": "Virgin Islands"},
                         {"label": "Virginia", "value": "Virginia"},
                         {"label": "Washington", "value": "Washington"},
                         {"label": "West Virginia", "value": "West Virginia"},
                         {"label": "Wisconsin", "value": "Wisconsin"},
                         {"label": "Wyoming", "value": "Wyoming"}],
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
def update_graph(slct_type):
    print(slct_type)
    print(type(slct_type))

    container = ""
    #"The value chosen by user was: {}".format(option_slctd)

    # Plotly Express
    fig = px.line(
        data_frame=df,
        x="date",
        y=slct_type,
        title="Growth of {}".format(slct_type)
    )
    return container, fig


@app.callback(
    [Output(component_id='output_container2', component_property='children'),
        Output('state_graph', 'figure')],
    [Input('slct_state', 'value'),
    Input('slct_new', 'value')]
)
def update_graph(slct_state, slct_new):
    print(slct_state)
    print(type(slct_state))

    container = ""

    dff = df1.copy()
    dff = dff[dff["state"] == slct_state]
    fig1 = px.line(
        data_frame=dff,
        x=slct_new,
        y="date",
        title="Growth of Cases"
    )

    return container, fig1


app.run_server(debug=True)
