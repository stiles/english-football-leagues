# English football data
Statistics and standings from the Premier League and League One. 

## Process

Several Python scripts collect data on past and current results, including: 

### Premier League

**Season results**
- Current table (live): `fetch_current_table.py`
    - *Automated with Github Actions workflow* 
    - *Runs daily to capture any mid-week fixures* 
- Past tables (historical): `fetch_past_tables.py`
    - *Output stored on S3*
    - *Used for reference*

### League One

**Season results**
- Current table (live): `fetch_league_one_table.py`
    - *Automated with Github Actions workflow*
    - *Runs daily for continuity with EPL workflow, which has mid-week fixtures*

## Outputs

### Premier League

**Season results tables**
- Historical (1992/93-2023/24): [JSON](https://stilesdata.com/football/table/epl_table_past.json), [CSV](https://stilesdata.com/football/table/epl_table_past.csv)
- Latest (2024-25): [JSON](https://stilesdata.com/football/table/epl_table_latest.json), [CSV](https://stilesdata.com/football/table/epl_table_latest.csv)
    - Season snapshots 
        - Base url: `https://stilesdata.com/football/table/season_snapshots/`
        - File name: `epl_table_latest_year_{YEAR}_week_{WEEK_NUMBER}.{JSON_CSV}`
        - Week 33 (opening week) example: [JSON](https://stilesdata.com/football/table/season_snapshots/epl_table_latest_year_2024_week_33.json), [CSV](https://stilesdata.com/football/table/season_snapshots/epl_table_latest_year_2024_week_33.csv)

**Example: Latest table**

The JSON file is a list of dictionaries. Each has the following items:

```json
    {
        "rk":5,
        "squad":"Tottenham",
        "mp":2,
        "w":1,
        "d":1,
        "l":0,
        "gf":5,
        "ga":1,
        "gd":4,
        "pts":4,
        "pts_mp":2.0,
        "xg":3.6,
        "xga":2.0,
        "xgd":1.6,
        "xgd_90":0.79,
        "last_5":"D W",
        "attendance":61357.0,
        "top_team_scorer":"Son Heung-min - 2",
        "goalkeeper":"Guglielmo Vicario",
        "notes":null,
        "season":"2024-2025",
        "fetched_date":"2024-08-31",
        "week_no":35
    }
```

### League One
**Season results tables**
- Latest (2024-25): [JSON](https://stilesdata.com/football/table/league_one_table_latest.json), [CSV](https://stilesdata.com/football/table/league_one_table_latest.csv)
    - Season snapshots 
        - Base url: `https://stilesdata.com/football/table/season_snapshots/`
        - File name: `league_one_table_latest_year_{YEAR}_week_{WEEK_NUMBER}.{JSON_CSV}`
        - Week 35 example: [JSON](https://stilesdata.com/football/table/season_snapshots/league_one_table_latest_year_2024_week_35.json), [CSV](https://stilesdata.com/football/table/season_snapshots/league_one_table_latest_year_2024_week_35.csv)

**Example: Latest table**

The JSON file is a list of dictionaries. Each has the following items:

```json
    {
        "team_id":"t109",
        "team_name":"Wrexham",
        "start_day_position":4,
        "current_position":2,
        "wins":3,
        "draws":1,
        "losses":0,
        "goals_for":8,
        "goals_against":2,
        "goal_difference":6,
        "table_points":10,
        "matches_played":4,
        "recent_form":"W,W,D,W",
        "week_number":35
    }
```

**Wrexham AFC fixtures**
- Latest season (2024-25): [JSON](https://stilesdata.com/football/fixtures/wrexham_game_logs_league_one_2024_2025.json), [CSV](https://stilesdata.com/football/fixtures/wrexham_game_logs_league_one_2024_2025.csv)


*More to come...*
