import plotly.express as px

from data import get_ny_times_state_wise_date, usa_data, get_state_wise_timeseries_date


def display_choropleth(select_category):
    new_df = usa_data()

    print('option selected ', select_category)
    column_to_use = select_category

    fig = px.choropleth(
        # title='Covid 19 Visualization in USA',
        data_frame=new_df,
        locationmode='USA-states',
        locations='Postal Code',
        scope="usa",
        color=column_to_use,
        hover_data=['Name', column_to_use],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'cases': '% of entire population'},
        template='plotly_dark'
    )

    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def growth_cases_graph(slct_type):
    print(slct_type)
    print(type(slct_type))

    container = ""
    #"The value chosen by user was: {}".format(option_slctd)

    # Plotly Express
    fig = px.line(
        data_frame=get_ny_times_state_wise_date(),
        x="date",
        y=slct_type,
        title="Growth of {}".format(slct_type)
    )
    return container, fig


def state_wise_timeseries(slct_state, slct_new):

    container = ""

    df = get_state_wise_timeseries_date()
    df = df[df["state"] == slct_state]
    fig1 = px.line(
        data_frame=df,
        x=slct_new,
        y="date",
        title="Growth of Cases"
    )

    return container, fig1
