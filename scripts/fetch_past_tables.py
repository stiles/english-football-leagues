import requests
import pandas as pd
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
    src = pd.read_html(url)[0]
    src['season'] = url.split('/')[-1].replace('-Premier-League-Stats', '')
    src.columns = src.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')
    src['squad'] = src['squad'].str.replace('Utd', "United").str.replace("Nott'ham", "Nottingham")
    seasons_dfs.append(src)
    sleep(randint(2,6))

# Concatenate results
df = pd.concat(seasons_dfs).drop_duplicates().reset_index(drop=True)

# Save json, csv file
df.to_json('../data/table/epl_table_past.json', indent=4, orient='records')
df.to_csv('../data/table/epl_table_past.csv', index=False)