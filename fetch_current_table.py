import pandas as pd
from datetime import datetime

# Dates/times (UTC)
week_number = datetime.now().isocalendar().week
current_year = datetime.now().year
next_year = current_year + 1
today = pd.Timestamp.today()
if today.month < 8:
    season = f"{today.year - 1}-{today.year}"
else:
    season = f"{today.year}-{today.year + 1}"

print("Season:", season)
today = pd.Timestamp.today().strftime('%Y-%m-%d')

# Outputs
JSON_OUT = 'data/table/epl_table_latest.json'
CSV_OUT = 'data/table/epl_table_latest.csv'
JSON_SNAPSHOT_OUT = f'data/table/season_snapshots/epl_table_latest_year_{current_year}_week_{week_number}.json'
CSV_SNAPSHOT_OUT = f'data/table/season_snapshots/epl_table_latest_year_{current_year}_week_{week_number}.csv'

# Define url
url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
print(url)

# Fetch table
df = pd.read_html(url)[0]

# Season
df['season'] = season

# Clean up columns, club names
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')
df['squad'] = df['squad'].str.replace('Utd', "United").str.replace("Nott'ham", "Nottingham")

# Add week number before exporting
df['fetched_date'] = today
df['week_no'] = week_number

# Export csv, json files
df.to_json(JSON_OUT, indent=4, orient='records')
df.to_csv(CSV_OUT, index=False)
df.to_json(JSON_SNAPSHOT_OUT, indent=4, orient='records')
df.to_csv(CSV_SNAPSHOT_OUT, index=False)