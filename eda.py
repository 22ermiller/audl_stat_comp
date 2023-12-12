import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read in Data
stats_df = pd.read_csv('player_season_stats.csv')

# Filter out players that haven't played very many points

filtered_df = stats_df[(stats_df['oPointsPlayed'] + stats_df['dPointsPlayed'] > 10*12) 
                       #& (stats_df['year'].isin([2015, 2023]))
                       ]

filtered_df['completion_percentage'] = filtered_df['completions']/filtered_df['throwAttempts']
filtered_df['minutes_played'] = filtered_df['secondsPlayed']/60


## Question 1: How many throwaways on average does each player throw every year

sns.boxplot(filtered_df, x = 'year', y = 'throwaways')
plt.title('Throwaway Distribution Comparison')
plt.xlabel('Throwaways')
plt.savefig('throwaway_comp.png')

## Question 2: Has completion percentage gone up?

sns.boxplot(filtered_df, x = 'year', y = 'completion_percentage')
plt.title('Completion Percentage Distribution Comparison')
plt.xlabel('Year')
plt.ylabel('Completion Percentage')
plt.savefig('completion_percentage.png')

## Question 3: Has number of blocks gone up?


# Grouping data by year and summing the blocks
blocks_by_year = filtered_df.groupby('year')['blocks'].sum()

# Creating a line plot
plt.figure(figsize=(8, 6))
blocks_by_year.plot(kind='line', marker='o', color='blue')
plt.xlabel('Year')
plt.ylabel('Number of Blocks')
plt.title('Blocks Per Year')
plt.savefig('block_nums.png')

## What about Callahans

# Grouping data by year and summing the blocks
callahans_by_year = filtered_df.groupby('year')['callahans'].sum()

# Creating a line plot
plt.figure(figsize=(8, 6))
callahans_by_year.plot(kind='line', marker='o', color='blue')
plt.xlabel('Year')
plt.ylabel('Number of Callahans')
plt.title('Callahans Per Year')
plt.savefig('callahan_nums.png')

## What about stalls

# Grouping data by year and summing the blocks
stalls_by_year = filtered_df.groupby('year')['stalls'].sum()

# Creating a line plot
plt.figure(figsize=(8, 6))
stalls_by_year.plot(kind='line', marker='o', color='blue')
plt.xlabel('Year')
plt.ylabel('Number of Stalls')
plt.title('Stalls Per Year')
plt.savefig('stall_nums.png')


# Question 5: Has the relationship between throwaways and assits changed at all?

# Filtering the DataFrame for specific years
selected_years = [2022, 2013]
filtered_years_df = filtered_df[filtered_df['year'].isin(selected_years)]

# Creating a scatter plot with regression lines for each year
sns.lmplot(data=filtered_years_df, x='throwaways', y='assists', hue='year', scatter=True, ci=None, markers='o',scatter_kws={'alpha': 0.5})
plt.title('Scatter Plot of Throwaways vs Assists For Specific Years')
plt.xlabel('Throwaways')
plt.ylabel('Assists')
plt.savefig('throwaway_v_assists.png')
# Question 6: How have pulls changed over the years

# Grouping data by year and summing the blocks
obpulls_by_year = filtered_df.groupby('year')['obPulls'].sum()

# Creating a line plot
plt.figure(figsize=(8, 6))
obpulls_by_year.plot(kind='line', marker='o', color='blue')
plt.title('OB Pulls Per Year')
plt.xlabel('Year')
plt.ylabel('OB Pulls')
plt.savefig('ob_pulls.png')
## Question 7: Has time played changed:


sns.boxplot(filtered_df, x = 'year', y = 'minutes_played')
plt.title('Minutes Played Distribution')
plt.xlabel('Year')
plt.ylabel('Minutes Played')
plt.savefig('minutes_played.png')
