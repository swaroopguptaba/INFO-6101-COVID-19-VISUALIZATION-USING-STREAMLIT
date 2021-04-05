import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import requests

app = dash.Dash(__name__)

covid_data = requests.get(
    'https://data.cdc.gov/resource/9mfq-cb36.json')

# print(covid_data)

df = pd.DataFrame(covid_data.json())
# print(df.head())
df.to_csv("/Users/balajianoopgupta/Documents/Swaroop_Docs/INFO 6101/group_by_state.csv", index=False)

print('before groupby :', df.shape)

df = df.groupby(['state'])["tot_cases", "new_case",
                           "tot_death"].apply(lambda x: x.astype(float).sum())

df.reset_index(inplace=True)
print('after groupby :', df.shape)
print(' data after groupby :', df.head())

print(df['state'].unique())
# get unique states
unique_states = df['state'].unique()

app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash",
            style={'text-align': 'center'}),

    dcc.RadioItems(
        id='slct_state',
        options=[{'value': x, 'label': x}
                 for x in unique_states],
        # value=unique_states[0],
        labelStyle={'display': 'inline-block'}
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


@ app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)

    container = "The state chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    print('option selected ', option_slctd)
    print('option type ', type(option_slctd))
    if(option_slctd != None):
        dff = dff[dff["state"] == option_slctd]
    else:
        # Plotly Express
        fig = px.choropleth(
            data_frame=dff,
            locationmode='USA-states',
            locations='state',
            scope="usa",
            color='tot_cases',
            hover_data=['state', 'tot_cases'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'tot_cases': '% of Total Deaths'},
            template='plotly_dark'
        )

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=False)
