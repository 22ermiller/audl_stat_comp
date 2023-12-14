import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("AUDL Yearly Metric Analysis")
st.write("A Dashboard that explores trends in different AUDL Metrics year over year.")

df = pd.read_csv("player_season_stats.csv")

st.subheader("Exploring Offensive Efficiency")
st.write("In this section, use the Year and Team selector to explore how the distribution of metrics that explore offensive efficiency have changed over time. View league wide trends by selecting all teams, or just look at trends within your favorite team. (Keep in mind, this data represents player data across a whole season, so outliers represent a value for a single player, not full game stats for a single team)")
st.write("For viewers unfamiliar with the AUDL, along with other teams, I would explore the empire as they've won 3 out of the last 4 championships (as of 2023). Keep in mind also, there has been a lot of turnover in AUDL franchises over that last 10 years. So if a team has no data for a certain year, it is most likely due to the fact that they weren't a part of the league that year, not missing data.")

left_column, right_column = st.columns(2)

year = left_column.multiselect(label='Select Years', options=df['year'].unique(), default=[2012, 2022])

team = right_column.multiselect('Select Teams', df['team'].unique(), df['team'].unique(), key='team1')

filtered_df = df[(df['year'].isin(year)) & df['team'].isin(team)]



left_column2, right_column2 = st.columns(2)

filtered_df['completion_percentage'] = filtered_df['completions']/filtered_df['throwAttempts']
filtered_df['minutes_played'] = filtered_df['secondsPlayed']/60

if not year:
    st.write('Select one or more years')
elif not team:
    st.write('Select one or more teams')
else:
    fig = px.box(filtered_df, x='year', y='completion_percentage', color='year',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "completion_percentage": "Completion Percentage"
                  },
                  title = "Completion Percentage Distribution Comparison")
    left_column2.plotly_chart(fig)
    left_column2.write("**In general, it seems that completition percentage has gone up and become less variable over the years")

if not year:
    st.write('Select one or more years')
elif not team:
    st.write('Select one or more teams')
else:
    fig = px.box(filtered_df, x='year', y='throwaways', color='year',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "throwaways": "Throwaways"
                  },
                  title = "Throwaway Distribution Comparison")
    right_column2.plotly_chart(fig)
    right_column2.write("**In general, it seems that the number of throwaways commited by a player over the course of a season has gone down and become less variable over the years")



if not year:
    st.write('Select one or more years')
elif not team:
    st.write('Select one or more teams')
else:
    temp_df = filtered_df
    temp_df['year'] = filtered_df['year'].astype(str)
    fig = px.scatter(temp_df, x="throwaways", y="assists", color='year',
                     trendline="ols",
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "assists": "Assists",
                      "throwaways": "Throwaways"
                  },
                  title = "Scatter Plot of Throwaways vs Assists For Specific Years")
    right_column2.plotly_chart(fig)
    right_column2.write("**Higher volume players get more assists, but also have more throwaways. A steeper slope on this graph would indicate less throwaways per assist and thus a more efficient player. Trends for this graph seem to be different team by team.")



st.subheader("Exploring Other Metrics")

st.write("In this section, we explore how metrics like number of blocks, and number of stalls change year over year. These also seem to be very different team by team. In these graphs, metrics are also split team by team for easier team comparison.")


team2 = st.multiselect('Select Teams', df['team'].unique(), ['shred', 'summit'], key='team2')
filtered_df2 = df[df['team'].isin(team2)]

left_column3, right_column3 = st.columns(2)


if not team2:
    st.write('Select one or more teams')
else:
    blocks_by_year = filtered_df2.groupby(['year', 'team'])['blocks'].sum().reset_index()
    blocks_by_year['year'] = blocks_by_year['year'].astype(str)
    fig = px.line(blocks_by_year, x="year", y="blocks", color='team',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "blocks": "Blocks",
                      "team" : "Team"
                  },
                  title = "Blocks Per Year")
    fig.update_xaxes(type='category')
    fig.update_traces(line=dict(width=3))  # Adjust the width as needed

# Add markers (points) at each data point
    fig.update_traces(mode='lines+markers', marker=dict(size=10))
    left_column3.plotly_chart(fig)


if not team2:
    st.write('Select one or more teams')
else:
    stalls_by_year = filtered_df2.groupby(['year', 'team'])['stalls'].sum().reset_index()
    stalls_by_year['year'] = stalls_by_year['year'].astype(str)
    fig = px.line(stalls_by_year, x="year", y="stalls",color='team',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "stalls": "Stalls",
                      "team" :"Team"
                  },
                  title = "Stalls Per Year")
    fig.update_xaxes(type='category')
    fig.update_traces(line=dict(width=3))  # Adjust the width as needed

# Add markers (points) at each data point
    fig.update_traces(mode='lines+markers', marker=dict(size=10))
    right_column3.plotly_chart(fig)

if not team2:
    st.write('Select one or more teams')
else:
    obPulls_by_year = filtered_df2.groupby(['year', 'team'])['obPulls'].sum().reset_index()
    obPulls_by_year['year'] = obPulls_by_year['year'].astype(str)
    fig = px.line(obPulls_by_year, x="year", y="obPulls",color='team',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "obPulls": "Out of Bounds Pulls",
                      "team" : "Team"
                  },
                  title = "Out of Bounds Pulls")
    fig.update_xaxes(type='category')
    fig.update_traces(line=dict(width=3))  # Adjust the width as needed

# Add markers (points) at each data point
    fig.update_traces(mode='lines+markers', marker=dict(size=10))
    left_column3.plotly_chart(fig)

if not team2:
    st.write('Select one or more teams')
else:
    callahans_by_year = filtered_df2.groupby(['year', 'team'])['callahans'].sum().reset_index()
    callahans_by_year['year'] = callahans_by_year['year'].astype(str)
    fig = px.line(callahans_by_year, x="year", y="callahans",color='team',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  labels={
                      "year": "Year",
                      "callahans": "Callahans",
                      "team" : "Team"
                  },
                  title = "Callahans Per Year")
    fig.update_xaxes(type='category')
    # Make the line thicker
    fig.update_traces(line=dict(width=3))  # Adjust the width as needed

# Add markers (points) at each data point
    fig.update_traces(mode='lines+markers', marker=dict(size=10))
    right_column3.plotly_chart(fig)

st.write("If you are interesting in learning more about how this data was collected and how I explored it initally click on the following links that lead to my blog posts:")

st.markdown(f'''
<a href={"https://22ermiller.github.io/blog/2023/12/01/project-data-generation.html"}><button style="background-color:GreenYellow;">Data Generation Blog Post</button></a>
''',
unsafe_allow_html=True)

#st.link_button("Data Generation Blog Post", "https://22ermiller.github.io/blog/2023/12/01/project-data-generation.html")
#st.link_button("EDA Blog Post","https://22ermiller.github.io/blog/2023/12/11/project-eda.html")

#st.write("Source code is all located at the following github repository:")

#st.link_button("GitHub Repository","https://github.com/22ermiller/audl_stat_comp/tree/main")