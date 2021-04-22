import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import numpy as np

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/bc60b7c7cefbc17a4e3fe6c3a6e86c65f88ca91d/us-states.csv", error_bad_lines=False)
#df = df.groupby(['state', 'date', 'cases', 'deaths'])
states = df['state'].unique()
states = np.sort(states)
states = list(states)



app.layout = html.Div([

    html.H1("GROWTH RATE", style={'text-align': 'center'}),

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
                     {"label": "District of Columbia", "value": "District of Columbia"},
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
                     {"label": "Northern Mariana Islands", "value": "Northern Mariana Islands"},
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

    container = "The State chosen by user was: {}".format(option_slctd)
    dff = df.copy()
    dff = dff[dff["state"] == option_slctd]

    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x = "cases",
        y = "date",
        title="Growth of Cases"
    )
    

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
