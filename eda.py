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

sns.boxplot(filtered_df, x = 'year', y = 'throwaways')
plt.title('Throwaway Distribution Comparison')
plt.savefig('throwaway_comp.png')