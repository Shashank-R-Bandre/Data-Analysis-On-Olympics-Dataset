"""
Run Code :- streamlit run app.py

pip install pipreqs
pipreqs --encoding=utf8
"""
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from PIL import Image

df = pd.read_csv('events.csv')
region_df = pd.read_csv('regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.header('Olympics Analysis')
st.sidebar.image('https://statathlon.com/wp-content/uploads/2018/01/rio-de-janeiro-2016-summer-olympics-e1467812135773.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_years_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally In ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + '\'s Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + '\'s Performance In ' + str(selected_year) + ' Olympics')

    st.table(medal_tally)


if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    st.title('Participating Nations Over The Year')
    image = Image.open('n_o_t.png')
    st.image(image, caption='Participating Nations Over The Year')

    st.title('Events Over The Year')
    image = Image.open('e_o_t.png')
    st.image(image, caption='Events Over The Year')

    st.title('Athletes Over The Year')
    image = Image.open('a_o_t.png')
    st.image(image, caption='Athletes Over The Year')


    st.title("Number Of Events Over Time For Every Sports")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select Country', country_list)
    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal Tally Over The Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' Excels In The Following Sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    # st.title('Top 10 Athletes Of ' + selected_country)
    # top10_df = helper.most_successful_countrywise(df,selected_country)
    # st.table(top10_df)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age Distribution', 'Gold Medalist', 'Sliver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=500)
    st.title('Athlete Age Distribution')
    st.plotly_chart(fig)




    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sports_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue=temp_df['Medal'], style=temp_df['Sex'], s=50)
    st.pyplot(fig)

    st.title('Men vs Women Participation Over The Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)