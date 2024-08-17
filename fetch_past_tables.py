import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
from tqdm.notebook import tqdm
from random import randint
from time import sleep

# Headers for requests
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

# Function to create season-specific urls
def generate_urls(base_url, start_year, num_years):
    urls = []
    for i in range(num_years):
        season_start = start_year - i
        season_end = season_start + 1
        season = f"{season_start}-{season_end}"
        url = base_url.format(season, season)
        urls.append(url)
    return urls

# Set up parameters
base_url = "https://fbref.com/en/comps/9/{}/{}-Premier-League-Stats"
current_year = datetime.now().year
start_year = current_year - 1
num_years = 32

# Generate URLs
urls = generate_urls(base_url, start_year, num_years)

# New list to store season dataframes
seasons_dfs = []

for url in tqdm(urls):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Wrap HTML in StringIO
    html_string = str(soup.select_one("table.stats_table"))
    html_io = StringIO(html_string)
    
    # Extract the first table
    table = pd.read_html(html_io)[0]
    
    # Extract the URLs for each team in the first table
    team_links = []
    table_rows = soup.select_one("table.stats_table").select("tbody tr")
    
    for row in table_rows:
        team_cell = row.select_one('td[data-stat="team"] a')
        if team_cell and "/squads/" in team_cell["href"]:
            team_links.append(f"https://fbref.com{team_cell['href']}")
        else:
            team_links.append(None)
    
    # Ensure the length of team_links matches the number of rows in the table
    if len(team_links) == len(table):
        table['team_url'] = team_links
    else:
        print(f"Warning: Mismatch in number of rows and team links for URL: {url}")
        print(f"Table rows: {len(table)}, Links found: {len(team_links)}")
        table['team_url'] = [None] * len(table)  # Fill with None to avoid errors
    
    table['season'] = url.split('/')[-1].replace('-Premier-League-Stats', '')
    table.columns = table.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')
    table['squad'] = table['squad'].str.replace('Utd', "United").str.replace("Nott'ham", "Nottingham")
    
    seasons_dfs.append(table)
    sleep(randint(2,6))

# Concatenate results
df = pd.concat(seasons_dfs).drop_duplicates().reset_index(drop=True)

# Save json, csv file
df.to_json('data/table/epl_table_past.json', indent=4, orient='records')
df.to_csv('data/table/epl_table_past.csv', index=False)