# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

'''
app.py: Frontend runner file for https://covid-streamlit-2021.herokuapp.com/

Dependencies
data: 
data/time_series_covid19.csv
time_series_covid19_confirmed_global.csv
time_series_covid19_deaths_global.csv
time_series_covid19_recovered_global.csv
cases_country.csv

modules:
frontend.py: Front-end works
generic.py: Load necessary files (infections, map)
'''

import streamlit as st
import pandas as pd
import generic
import frontend
import pydeck as pdk
import math
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import folium
import numpy as np
from datetime import date


filename = 'https://github.com/staedi/nCOV-summary/raw/master/time_series_covid19.csv'

################################################################
# Header and preprocessing

# Set Title
st.title('Covid-19 News and Dashboard')

# Initial data load
update_status = st.markdown("Loading infections data...")
covid = generic.read_dataset(filename)
update_status.markdown('Load complete!')



################################################################
# Sidebar section
sel_region, sel_country, chosen_stat, sel_map = frontend.display_sidebar(covid)


################################################################
# Main section
update_status.markdown("Finding top districts...")
cand = generic.set_candidates(covid,sel_region,sel_country,chosen_stat)
update_status.markdown("Calculation complete!")

update_status.markdown("Drawing charts")
if sel_map:
    update_status.markdown("Drawing charts & maps...")
else:
    update_status.markdown("Drawing charts...")
frontend.show_stats(covid,sel_region,sel_country,chosen_stat,cand,sel_map)
update_status.markdown("Job Complete!")


# NOT USING THE pygooglenewsapi, it's deprecated
# -----------------------------------

# # Covid-19 News Feed Searcher

# -----------------------------------
# '''

# gn = GoogleNews()

# search_term = st.text_input('Search for Covid News:', 'Covid-19')
# search_range = st.slider('Search Range (days):', 1, 365, 1)

# search = gn.search(search_term, when=f'{search_range}d')

# data = pd.DataFrame.from_dict(search['entries'])

# f'''
# # {search_term} News Articles
# Last *{search_range} day/s*

# ------------------------------------------- 
# '''

# # Display articles found
# for row in range(1, data.shape[1]):

#     f'''
#     ## {data['published'].iloc[row]}
#     ### {data['title'].iloc[row]}
#     Link: {data['link'].iloc[row]}
    
#     ------------------------------------------- 
#     '''


################################################################
# Dataset for Exploratory Data Analysis
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


# Adding multiple themes, including light and dark mode
if st.checkbox('Dark Mode'):
    st.markdown("""
    <style>
    :root, img, video, h1,h2, h3, h4, .highlight, iframe, .svg-container{
        filter: invert(100%) hue-rotate(180deg);
        color: white;
    }
    .element-container h2{
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


confirmed_total = int(country_df['Confirmed'].sum())
active_total = int(country_df['Active'].sum())
deaths_total = int(country_df['Deaths'].sum())
recovered_total = int(country_df['Recovered'].sum())

# Data Preprocessing
country_df['Incident_Rate'].fillna(0, inplace=True)
country_df['Mortality_Rate'].fillna(0, inplace=True)
country_df['Active'] = country_df['Active'].apply(lambda x : 0 if x < 0 else x)

# helper function
def breakline():
    return st.markdown("<br>", unsafe_allow_html=True)

#################### STATS : Confirmed, Active, Deaths, Recovered ####################
breakline()
st.markdown("""
<style>
.highlight {
  border-radius: 0.5rem;
  color: black;
  padding: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
}
.bold {
  padding-left: 0.3rem;
  padding-right: 0.3rem;
  font-weight: 500;
}
.red {
  background-color: lightcoral;
}
.blue {
  background-color: lightblue;
}
.green {
  background-color: lightgreen;
}
.yellow {
  background-color: yellow;
}
.center{
  text-align : center; 
}
</style>            
""", unsafe_allow_html=True)

t = "<div class='center'> | Confirmed : <span class='highlight blue bold'>" + str(confirmed_total) + "</span> | Active : <span class='highlight yellow bold'>"+ str(active_total) +"</span> | Deaths : <span class='highlight red bold'>"+ str(deaths_total) +"</span> | Recovered : <span class='highlight green bold'>"+ str(recovered_total) +"</span> |</div><br><br>"
st.markdown(t, unsafe_allow_html=True)


############# Plot for Confirmed, Recovered and Death cases across world ############
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Covid-19 across the world</h2>",
            unsafe_allow_html=True)
breakline()
df_list = []
labels = []
colors = []
colors_dict =  {
        'Confirmed' : 'blue',
        'Deaths' : 'red',
        'Recovered' : 'green'
    }
features = st.multiselect("Select display features : ", 
                          ['Confirmed', 'Deaths', 'Recovered'],
                          default = ['Confirmed','Recovered','Deaths'],
                          key = 'world_features')
for feature in features:
    if feature == 'Confirmed':
        labels.append('Confirmed')
        colors.append(colors_dict['Confirmed'])
        df_list.append(confirmed_df)
    if feature == 'Deaths':
        labels.append('Deaths')
        colors.append(colors_dict['Deaths'])
        df_list.append(death_df)
    if feature == 'Recovered':
        labels.append('Recovered')
        colors.append(colors_dict['Recovered'])
        df_list.append(recovered_df)


# Plot confirmed, active, death, recovered cases
def plot_cases_of_world():
    line_size = [4, 5, 6]
    
    fig = go.Figure();
    
    for i, df in enumerate(df_list):
        x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df.iloc[:,4:]),axis = 0)
            
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels[i]) +": "+ str(y_data[-1])
        ));
    
    fig.update_layout(
        title="COVID-19 cases of World",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 800,
        
    );
    
    fig.update_yaxes(type="linear")
    st.plotly_chart(fig);

plot_cases_of_world()
######################################################################################


########### Plot for Confirmed, Recovered and Death cases across countries ########### 
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Covid-19 across countries</h2>",
            unsafe_allow_html=True)
st.write("## Covid-19 across countries")
breakline()
df_list2 = []
labels2 = []
colors2 = []
colors_dict2 =  {
        'Confirmed' : 'blue',
        'Deaths' : 'red',
        'Recovered' : 'green'
    }
selected_country = st.selectbox('Select Country : ', tuple(country_df.iloc[:, 0]), 79)
features2 = st.multiselect("Select display features : ", 
                           ['Confirmed', 'Deaths', 'Recovered'],
                           default = ['Confirmed', 'Deaths', 'Recovered'],
                           key = 'country_features')
for feature in features2:
    if feature == 'Confirmed':
        labels2.append('Confirmed')
        colors2.append(colors_dict2['Confirmed'])
        df_list2.append(confirmed_df)
    if feature == 'Deaths':
        labels2.append('Deaths')
        colors2.append(colors_dict2['Deaths'])
        df_list2.append(death_df)
    if feature == 'Recovered':
        labels2.append('Recovered')
        colors2.append(colors_dict2['Recovered'])
        df_list2.append(recovered_df)

# Plot confirmed, active, death, recovered cases
def plot_cases_of_countries(country):
    line_size = [4, 5, 6]
    
    fig = go.Figure();
    
    for i, df in enumerate(df_list2):
        x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df[df.iloc[:,1] == country].iloc[:, 4:]),axis = 0)
        
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels2[i],
        line=dict(color=colors2[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels2[i]) +": "+ str(y_data[-1])
        ));
    
    fig.update_layout(
        title="COVID-19 cases of " + country,
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 800,
        
    );
    
    fig.update_yaxes(type="linear")
    st.plotly_chart(fig);

# default selected country is India in dropdown
breakline()
plot_cases_of_countries(selected_country)
#############################################################


################# Countries With Most Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with most number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Active', 'Deaths', 'Recovered'],
                            key = 'most_cases')
selected_count = st.slider('No. of countries :', 
                           min_value=1, max_value=50, 
                           value=10, key='most_count')
sorted_country_df = country_df.sort_values(type_of_case, ascending= False) 
def bubble_chart(n):
    fig = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
               hover_name="Country_Region", size_max=60)
    fig.update_layout(
    title=str(n) +" Countries with most " + type_of_case.lower() + " cases",
    xaxis_title="Countries",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )
    st.plotly_chart(fig);
bubble_chart(selected_count)
#############################################################


################# Countries With Least Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with least number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Active', 'Deaths', 'Recovered'],
                            key = 'least_cases')
selected_count = st.slider('No. of countries :', 
                           min_value=1, max_value=50, 
                           value=10, key = 'least_cases')
sorted_country_df = country_df[country_df[type_of_case] > 0].sort_values(type_of_case, ascending= True)
def bubble_chart(n):
    fig = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
               hover_name="Country_Region", size_max=60)
    fig.update_layout(
    title=str(n) +" Countries with least " + type_of_case.lower() + " cases",
    xaxis_title="Countries",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )   
    st.plotly_chart(fig);
bubble_chart(selected_count)

#############################################################


####################### Incident & Mortality Rates #######################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Incident & Mortality Rates</h2>",
            unsafe_allow_html=True)
st.write("### View info for : ")
option_selected = st.radio("", options=['Country', 'Distributions'])
if option_selected == 'Country':
    country = st.selectbox("Select country :", tuple(country_df.iloc[:, 0]), 79)
    
    rates = country_df[country_df['Country_Region'] == country][['Incident_Rate','Mortality_Rate']]
    text = "<div class='center bold'> Incident Rate : <span class='highlight yellow bold'>" + "{:.4f}".format((rates.iloc[0,0])) + "</span> | Mortality Rate : <span class='highlight red bold'>"+ "{:.4f}".format((rates.iloc[0,1])) +"</span> </div><br><br>"
    st.markdown(text, unsafe_allow_html=True)    


else:
    inc_rates = country_df['Incident_Rate']
    mort_rates = country_df['Mortality_Rate']
        
    hist_data = [inc_rates]
    group_labels = ['Incident Rates']
    colors = ['rgb(0, 0, 100)']
    fig1 = ff.create_distplot(hist_data, group_labels, colors=colors,
                             bin_size=500, show_rug=False)
    # Add title
    fig1.update_layout(title_text='Distribution of Incident Rates', 
                       annotations=[dict(x=0.5, y=-0.15, showarrow=False,
                                         text="Incident Rates",
                                         xref="paper", yref="paper")])
    
    hist_data = [mort_rates]
    group_labels = ['Mortality Rates']
    colors = ['rgb(0, 200, 200)']
    fig2 = ff.create_distplot(hist_data, group_labels, colors=colors,
                             bin_size=3 , show_rug=False)
    # Add title
    fig2.update_layout(title_text='Distribution of Mortality Rates', 
                       annotations=[dict(x=0.5, y=-0.15, showarrow=False,
                                         text="Mortality Rates",
                                         xref="paper", yref="paper")])

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
 

st.write("### View plots for : ")
opt_selected = st.radio("", options=['Top & Bottom Incident Rates', 'Top & Bottom Mortality Rates'])
if opt_selected == 'Top & Bottom Incident Rates':
    country_count = st.slider('No. of countries :', 
                              min_value=2, max_value=10, 
                              value=5, key='incident_count')
    
    # Top Incident Rates
    table_data = country_df[['Country_Region', 'Incident_Rate']].sort_values('Incident_Rate', ascending=False).head(country_count)
    table_data['Incident_Rate'] = table_data['Incident_Rate'].apply(lambda x:round(x,4))
    
    fig1 = ff.create_table(table_data, height_constant=60)
    trace1 = go.Bar(x=table_data['Country_Region'], y=table_data['Incident_Rate'], 
                    xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099ff'),
                    name='')
    
    fig1.add_traces([trace1])
    
    fig1['layout']['xaxis2'] = {}
    fig1['layout']['yaxis2'] = {}
    
    fig1.layout.xaxis.update({'domain': [0, .4]})
    fig1.layout.xaxis2.update({'domain': [0.5, 1.]})
    
    fig1.layout.yaxis2.update({'anchor': 'x2'})
    fig1.layout.yaxis2.update({'title': 'Incident Rates'})
    
    fig1.layout.margin.update({'t':50, 'b':0})
    
    # Donut chart
    labels = table_data['Country_Region']
    values = table_data['Incident_Rate']
    # Use `hole` to create a donut-like pie chart
    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    
    # Bottom Incident Rates
    temp_df = country_df[['Country_Region', 'Incident_Rate']]
    table_data = temp_df[temp_df['Incident_Rate'] > 0].sort_values('Incident_Rate', ascending=True).head(country_count)
    table_data['Incident_Rate'] = table_data['Incident_Rate'].apply(lambda x:round(x,4))
    
    fig2 = ff.create_table(table_data, height_constant=60)
    trace2 = go.Bar(x=table_data['Country_Region'], y=table_data['Incident_Rate'], 
                    xaxis='x2', yaxis='y2',
                    marker=dict(color='crimson'),
                    name='')
    
    fig2.add_traces([trace2])
    
    fig2['layout']['xaxis2'] = {}
    fig2['layout']['yaxis2'] = {}
    
    fig2.layout.xaxis.update({'domain': [0, .4]})
    fig2.layout.xaxis2.update({'domain': [0.5, 1.]})
    
    fig2.layout.yaxis2.update({'anchor': 'x2'})
    fig2.layout.yaxis2.update({'title': 'Incident Rates'})
    
    fig2.layout.margin.update({'t':50, 'b':0})
    
    # Donut chart
    labels = table_data['Country_Region']
    values = table_data['Incident_Rate']
    # Use `hole` to create a donut-like pie chart
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    
    st.write("### Top " + str(country_count) + " Incident Rates ")
    st.plotly_chart(fig1)
    if st.checkbox('Show donut chart', key='top_inc'):
        st.plotly_chart(fig3)
    st.write("### Bottom " + str(country_count) + " Incident Rates ")
    st.plotly_chart(fig2)
    if st.checkbox('Show donut chart    ', key='bottom_inc'):
        st.plotly_chart(fig4)
  
    
else:
    country_count = st.slider('No. of countries :', 
                              min_value=2, max_value=10, 
                              value=5, key='mortality_count')
    
    # Top Mortality Rates
    table_data = country_df[['Country_Region', 'Mortality_Rate']].sort_values('Mortality_Rate', ascending=False).head(country_count)
    table_data['Mortality_Rate'] = table_data['Mortality_Rate'].apply(lambda x:round(x,4))
    fig1 = ff.create_table(table_data, height_constant=60)
    
    trace1 = go.Bar(x=table_data['Country_Region'], y=table_data['Mortality_Rate'], 
                    xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099ff'),
                    name='')
    
    fig1.add_traces([trace1])
    
    fig1['layout']['xaxis2'] = {}
    fig1['layout']['yaxis2'] = {}
    
    fig1.layout.xaxis.update({'domain': [0, .4]})
    fig1.layout.xaxis2.update({'domain': [0.5, 1.]})
    
    fig1.layout.yaxis2.update({'anchor': 'x2'})
    fig1.layout.yaxis2.update({'title': 'Mortality Rates'})
    
    fig1.layout.margin.update({'t':50, 'b':0})
    
    # Donut chart
    labels = table_data['Country_Region']
    values = table_data['Mortality_Rate']
    # Use `hole` to create a donut-like pie chart
    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    
    # Bottom Mortality Rates
    temp_df = country_df[['Country_Region', 'Mortality_Rate']]
    table_data = temp_df[temp_df['Mortality_Rate'] > 0].sort_values('Mortality_Rate', ascending=True).head(country_count)
    table_data['Mortality_Rate'] = table_data['Mortality_Rate'].apply(lambda x:round(x,4))
    fig2 = ff.create_table(table_data, height_constant=60)
    
    trace2 = go.Bar(x=table_data['Country_Region'], y=table_data['Mortality_Rate'], 
                    xaxis='x2', yaxis='y2',
                    marker=dict(color='crimson'),
                    name='')
    
    fig2.add_traces([trace2])
    
    fig2['layout']['xaxis2'] = {}
    fig2['layout']['yaxis2'] = {}
    
    fig2.layout.xaxis.update({'domain': [0, .4]})
    fig2.layout.xaxis2.update({'domain': [0.5, 1.]})
    
    fig2.layout.yaxis2.update({'anchor': 'x2'})
    fig2.layout.yaxis2.update({'title': 'Mortality Rates'})
    
    fig2.layout.margin.update({'t':50, 'b':0})
    
    # Donut chart
    labels = table_data['Country_Region']
    values = table_data['Mortality_Rate']
    # Use `hole` to create a donut-like pie chart
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    
    st.write("### Top " + str(country_count) + " Mortality Rates ")
    st.plotly_chart(fig1)
    if st.checkbox("Show donut chart", key='top_mortal'):
        st.plotly_chart(fig3)
    st.write("### Bottom " + str(country_count) + " Mortality Rates ")
    st.plotly_chart(fig2)
    if st.checkbox("Show donut chart", key='bottom_mortal'):
        st.plotly_chart(fig4)
################################################################################


############################# Time Series Analysis #############################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Time Series Analysis</h2>",
            unsafe_allow_html=True)
country = st.selectbox("Select country :", tuple(country_df.iloc[:, 0]), 79, key='time_series')
case_type = st.selectbox("Select case type : ", ['Confirmed', 'Deaths', 'Recovered'])
month_week_date = st.selectbox("Select how you want to plot data :", ['By Weeks','By Months', 'By Date'])
case_dict = {
        'Confirmed' : confirmed_df,
        'Deaths' : death_df,
        'Recovered' : recovered_df
    }
start_date = case_dict[case_type].columns[4].split('/') # 0-month, 1-day, 2-year
end_date = case_dict[case_type].columns[-1].split('/')  # 0-month, 1-day, 2-year  
date1 = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
date2 = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
days = abs(date1 - date2).days

if month_week_date == 'By Months':
    months = days//30
    month_slider = st.slider("Select range of months :", 1, months+1, (1, months+1))
    temp_df = case_dict[case_type]
    temp_df = temp_df.iloc[:, 1: 4+(month_slider[1]-1)*30]
    x_data = np.array(list(temp_df.iloc[:, 3+(month_slider[0]-1)*30 : 3+(month_slider[1]-1)*30].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].iloc[:, 3+(month_slider[0]-1)*30 : 3+(month_slider[1]-1)*30], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Months",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)
    
    
elif month_week_date == 'By Weeks':
    weeks = days // 7
    week_slider = st.slider("Select range of weeks :",1, weeks, (1,weeks))
    temp_df = case_dict[case_type]
    temp_df = temp_df.iloc[:, 1: 4+(week_slider[1]-1)*7]
    x_data = np.array(list(temp_df.iloc[:, 3+(week_slider[0]-1)*7 : 3+(week_slider[1]-1)*7].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].iloc[:, 3+(week_slider[0]-1)*7 : 3+(week_slider[1]-1)*7], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Weeks",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)

else:
    full_date_range = list(case_dict[case_type].iloc[:, 4:].columns)
    date_slider = st.select_slider(
        "Choose date range (M/DD/YY) :", full_date_range,
        (full_date_range[0], full_date_range[-1]))
    temp_df = case_dict[case_type]
    temp_df = temp_df.loc[:, 'Country/Region':date_slider[1]]
    x_data = np.array(list(temp_df.loc[:, date_slider[0] : date_slider[1]].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].loc[:, date_slider[0] : date_slider[1]], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Date",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)


######################## Countries with zero cases #######################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with zero cases</h2>",
            unsafe_allow_html=True)
case_type = st.selectbox("Select case type : ", 
                         ['Confirmed', 'Active', 'Deaths', 'Recovered'], 1,
                         key= 'zero_cases')
temp_df = country_df[country_df[case_type] == 0]
st.write('### Countries with zero ' + case_type.lower() + ' cases :')
if len(temp_df) == 0:
    st.error('Sorry. There are no records present where ' + case_type.lower() + ' cases are zero!')
else:
    temp_df = temp_df[['Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    st.write(temp_df)
##########################################################################

# Data Resource Credits
st.subheader('Resource Credits')
data_source = 'Johns Hopkins University CSSE'
if sel_region == 'KOR':
    data_source = 'KCDC'
elif not sel_region:
    data_source += ', KCDC'
st.write('Data source: ' + data_source)
st.write('Map shapedata: Natural Earth')
st.write('Map provider: Mapbox, OpenStreetMap')
