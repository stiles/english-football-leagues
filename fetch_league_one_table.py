import requests
import pandas as pd
from datetime import datetime

# Date variables
week_number = datetime.now().isocalendar().week
current_year = datetime.now().year
today = pd.Timestamp.today().strftime('%Y-%m-%d')

# Headers for requests
headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# Which league and season
params = {
    'competitionID': '11',
    'seasonID': current_year,
}

# Make the request for table JSON
response = requests.get(
    'https://multi-club-matches.webapi.gc.eflservices.co.uk/v2/league-tables',
    params=params,
    headers=headers,
)

# Extract table list from JSON
table_list = response.json()['data']

# Fresh list to store team details
team_list = []

# Loop through teams, extracting items into a list of dictionaries
for team in table_list:
    attributes = team['attributes']

    team_list.append({
        'team_id': team['id'],
        'team_name': attributes['teamName'],
        'start_day_position': attributes['startDayPosition'],
        'current_position': attributes['position'],
        'wins': attributes['won'],
        'draws': attributes['drawn'],
        'losses': attributes['lost'],
        'goals_for': attributes['goalsFor'],
        'goals_against': attributes['goalsAgainst'],
        'goal_difference': attributes['goalDifference'],
        'table_points': attributes['points'],
        'matches_played': attributes['played'],
        'recent_form': attributes['form'],
        "week_number": week_number,
    })

# Convert list of dicts to DataFrame
df = pd.DataFrame(team_list)

# Export JSON and CSV
df.to_json('data/table/league_one_table_latest.json', indent=4, orient='records')
df.to_csv('data/table/league_one_table_latest.csv', index=False)

# Snapshots
df.to_json(f'data/table/season_snapshots/league_one_table_latest_year_{current_year}_week_{week_number}.json', indent=4, orient='records')
df.to_csv(f'data/table/season_snapshots/league_one_table_latest_year_{current_year}_week_{week_number}.csv', index=False)