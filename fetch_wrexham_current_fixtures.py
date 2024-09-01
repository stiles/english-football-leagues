import json
import requests
import pandas as pd
from datetime import datetime

# Dates/times (UTC)
week_number = datetime.now().isocalendar().week
current_year = datetime.now().year
next_year = current_year + 1
season = f"{current_year}_{next_year}"
today = pd.Timestamp.today().strftime('%Y-%m-%d')
season_start = f"{current_year}-08-01"

# Define the API endpoint and headers
headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# Endpoint for all Wrexham matches
# last season in League 2: 
# https://multi-club-matches.webapi.gc.eflservices.co.uk/v2/matches?from=2023-08-01%2000:00:00Z&to=2024-08-31%2023:59:59Z&competitionID=12&seasonID=2023&page.size=200&teamID=t109

# Create the URL with dynamic date parameters
url = (
    f"https://multi-club-matches.webapi.gc.eflservices.co.uk/v2/matches"
    f"?from={season_start} 00:00:00Z&to={today} 23:59:59Z"
    f"&competitionID=11&seasonID={current_year}&page.size=100&teamID=t109"
)

response = requests.get(url, headers=headers)

# Parse the JSON response
data = response.json()

# List to store match details
matches = []

# Loop through each match and extract relevant information
for match in data['data']:
    attributes = match['attributes']
    
    # Determine if Wrexham is the home or away team
    if attributes['homeTeam']['name'] == "Wrexham":
        home_away = "home"
        opponent = attributes['awayTeam']['name']
        wrexham_score = attributes['homeTeam']['score']
        opponent_score = attributes['awayTeam']['score']
        wrexham_half_score = attributes['homeTeam']['halfScore']
        opponent_half_score = attributes['awayTeam']['halfScore']
        penalty_score = attributes['homeTeam']['penaltyScore']
    else:
        home_away = "away"
        opponent = attributes['homeTeam']['name']
        wrexham_score = attributes['awayTeam']['score']
        opponent_score = attributes['homeTeam']['score']
        wrexham_half_score = attributes['awayTeam']['halfScore']
        opponent_half_score = attributes['homeTeam']['halfScore']
        penalty_score = attributes['awayTeam']['penaltyScore']
    
    # Create a dictionary for the match
    match_info = {
        "kickoff_date_utc": attributes['kickOffDateUTC'],
        "home_away": home_away,
        "opponent": opponent,
        "wrexham_score": wrexham_score,
        "opponent_score": opponent_score,
        "wrexham_half_score": wrexham_half_score,
        "opponent_half_score": opponent_half_score,
        "penalty_score": penalty_score,
        "match_minutes": attributes['matchMinutes'],
        "match_period": attributes['matchPeriod'],
        "formatted_matchtime": attributes['formattedMatchTime'],
        "resultType": attributes['resultType'],
        "postponement_reason": attributes['postponementReason'],
        "matchWinner": attributes['matchWinner']['name'] if attributes.get('matchWinner') else None # Handle missing 'matchWinner'
    }
    
    # Append the match info to the list
    matches.append(match_info)

# Convert the list of matches to a DataFrame
df = pd.DataFrame(matches)

df.to_json(f'data/fixtures/wrexham_match_logs_league_one_{season}.json', indent=4, orient='records')
df.to_csv(f'data/fixtures/wrexham_match_logs_league_one_{season}.csv', index=False)