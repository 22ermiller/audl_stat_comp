import pandas as pd
import numpy as np
import requests
import re
import urllib.parse
import re
import math

base_url = "https://www.backend.audlstats.com/api/v1/"

## Get A List of Players ##

# Players Endpoint
players_endpoint = base_url + "players"

# get years 2015-2023
params = {'years': ['2015,2016,2017,2018,2019,2020,2021,2022,2023']}
r = requests.get(players_endpoint, params=params)
players = r.json()

players_data = players['data']  # Access the 'data' key from the JSON response
players_list = []
for player in players_data:
    teams = player['teams']
    for team in teams:
        player_info = {
            'id': player['playerID'],
            'firstName': player['firstName'],
            'lastName': player['lastName'],
            'year': team['year'] if player['teams'] else None,  # Accessing the 'year' within 'teams' list
            'team': team['teamID']
        }
        players_list.append(player_info)

players_df = pd.DataFrame(players_list)

## Use Player list to Get players stats each year ##

# create list of unique player ids

player_ids = players_df['id'].unique()

# Player Stats Endpoint

stats_endpoint = base_url + 'playerStats'

# Loop through list of players in groups of 100
batch_size = 100
num_batches = math.ceil(len(player_ids)/100)

# Initialize stats_df

stats_df = pd.DataFrame()

for i in range(num_batches):
    start_index = i * batch_size
    end_index = (i + 1) * batch_size
    batch_ids = player_ids[start_index:end_index]

    # Make API call with the batch of player IDs
    params = {'playerIDs': ','.join(map(str, batch_ids))}
    r = requests.get(stats_endpoint, params=params)
    stats = r.json()
    stats_data = stats['data']
    names = [{'firstName': player['player']['firstName'], 'lastName': player['player']['lastName']} 
                 for player in stats_data]
        
    # Create a DataFrame for the batch of stats
    batch_df = pd.DataFrame(stats_data)
        
    # Create a DataFrame for names and merge with batch_df
    names_df = pd.DataFrame(names)
    batch_df = pd.concat([batch_df, names_df], axis=1)


    # Append to final df
    stats_df = stats_df.append(batch_df, ignore_index = True)



final_df = stats_df.drop(columns = 'player')

final_df = pd.merge(final_df, players_df, how='left', left_on=['year', 'firstName', 'lastName'],right_on=['year', 'firstName', 'lastName'])

final_df.to_csv('player_season_stats.csv', index = False)