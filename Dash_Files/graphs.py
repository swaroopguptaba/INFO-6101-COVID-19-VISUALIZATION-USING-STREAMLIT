import plotly.express as px

from data import usa_data


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
