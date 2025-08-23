import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from io import StringIO
try:
    import cloudscraper  # type: ignore
except Exception:  # pragma: no cover
    cloudscraper = None
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

# Headers for requests
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'referer': 'https://fbref.com/',
}

df = None

# Try fbref first; on failure we will fall back to the PL API
try:
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, timeout=30)

    if response.status_code == 403 and cloudscraper is not None:
        scraper = cloudscraper.create_scraper()
        scraper.headers.update(headers)
        response = scraper.get(url, timeout=30)
    elif response.status_code == 403:
        mirror_url = f"https://r.jina.ai/http://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
        response = session.get(mirror_url, timeout=30)

    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table_tag = soup.select_one('table.stats_table')

    if table_tag is not None:
        html_io = StringIO(str(table_tag))
        df = pd.read_html(html_io)[0]
    else:
        comment_tables_html = []
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if 'table' in comment and 'stats_table' in comment:
                comment_tables_html.append(str(comment))
        if comment_tables_html:
            html_io = StringIO(comment_tables_html[0])
            df = pd.read_html(html_io)[0]
        else:
            tables = pd.read_html(response.text)
            selected = None
            for t in tables:
                cols = t.columns.tolist()
                flat_cols = [c if isinstance(c, str) else ' '.join(map(str, c)) for c in cols]
                if any(('Squad' in col) or ('Team' in col) for col in flat_cols):
                    selected = t
                    break
            df = selected if selected is not None else tables[0]
except Exception:
    df = None

# Fallback to Premier League API if fbref is blocked or parsing failed
if df is None or df is not None and ('Squad' not in df.columns and 'squad' not in df.columns):
    api_headers = {
        'user-agent': headers['user-agent'],
        'accept': 'application/json',
        'origin': 'https://www.premierleague.com',
        'referer': 'https://www.premierleague.com/tables',
        'accept-language': headers['accept-language'],
    }

    season_start = int(season.split('-')[0])
    season_end_two = str(int(season.split('-')[1]))[-2:]
    season_label = f"{season_start}/{season_end_two}"

    cs_resp = requests.get(
        'https://footballapi.pulselive.com/football/competitions/1/compseasons',
        headers=api_headers,
        params={'page': 0, 'pageSize': 50},
        timeout=30,
    )
    cs_resp.raise_for_status()
    cs_data = cs_resp.json()
    comp_season_id = None
    for item in cs_data.get('content', []):
        if item.get('label') == season_label:
            try:
                comp_season_id = int(float(item.get('id')))
            except Exception:
                comp_season_id = int(str(item.get('id')).split('.')[0])
            break
    if comp_season_id is None and cs_data.get('content'):
        try:
            comp_season_id = int(float(cs_data['content'][0]['id']))
        except Exception:
            comp_season_id = int(str(cs_data['content'][0]['id']).split('.')[0])

    st_resp = requests.get(
        'https://footballapi.pulselive.com/football/standings',
        headers=api_headers,
        params={'comps': 1, 'compSeasons': comp_season_id, 'altIds': 'true', 'detail': 2},
        timeout=30,
    )
    st_resp.raise_for_status()
    standings = st_resp.json()
    entries = standings['tables'][0]['entries']

    rows = []
    for e in entries:
        team_name = e['team']['name']
        overall = e['overall']
        rows.append({
            'rk': e.get('position'),
            'squad': team_name,
            'mp': overall.get('played'),
            'w': overall.get('won'),
            'd': overall.get('drawn'),
            'l': overall.get('lost'),
            'gf': overall.get('goalsFor'),
            'ga': overall.get('goalsAgainst'),
            'gd': overall.get('goalsDifference'),
            'pts': overall.get('points'),
        })

    df = pd.DataFrame(rows)

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