import pytz
import requests
import pandas as pd

# Tottenham page url
url = "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats"

# DataFrame
df = pd.read_html(url)[0]

# Clean up
df.columns = df.columns.str.lower().str.replace(" ", "_")
df["round"] = df["round"].str.replace("Matchweek ", "")
df["opponent"] = (
    df["opponent"].str.replace("Nott'ham", "Nottingham").str.replace("Utd", "United")
)
# Combine the date and time columns into a single datetime column
df["datetime_uk"] = pd.to_datetime(df["date"] + " " + df["time"])

# Define the time zones
uk_timezone = pytz.timezone("Europe/London")
pst_timezone = pytz.timezone("America/Los_Angeles")

# Localize the datetime to UK time
df["datetime_uk"] = df["datetime_uk"].dt.tz_localize(uk_timezone)
df["day"] = df["datetime_uk"].dt.day_name()

# Convert the UK time to PST
df["date_pst"] = df["datetime_uk"].dt.tz_convert(pst_timezone).dt.strftime("%Y-%m-%d")
df["time_pst"] = df["datetime_uk"].dt.tz_convert(pst_timezone).dt.strftime("%H:%M")

# Optimize columns
df_slim = df[
    [
        "date",
        "time",
        "round",
        "day",
        "venue",
        "result",
        "gf",
        "ga",
        "opponent",
        "poss",
        "attendance",
        "captain",
        "formation",
        "opp_formation",
        "date_pst",
        "time_pst",
    ]
]

# Export json, csv
df_slim.to_json(
    "../data/schedule/tottenham_schedule_latest.json", indent=4, orient="records"
)
df_slim.to_csv("../data/schedule/tottenham_schedule_latest.csv", index=False)