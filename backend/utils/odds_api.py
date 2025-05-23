import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"
SPORT = "basketball_nba"  # or americanfootball_nfl

def get_upcoming_events():
    url = f"{BASE_URL}/sports/{SPORT}/events/"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Events error {response.status_code}: {response.text}")
    return response.json()

def get_event_props(event_id):
    url = f"{BASE_URL}/events/{event_id}/odds/"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Props error {response.status_code}: {response.text}")
    return response.json()

def get_player_props(market_key="player_points", max_events=5):
    events = get_upcoming_events()
    all_props = []

    for event in events[:max_events]:
        event_id = event["id"]
        home = event["home_team"]
        away = event["away_team"]

        try:
            props_data = get_event_props(event_id)
        except Exception as e:
            print(f"Skipping event {event_id} due to error: {e}")
            continue

        for bookmaker in props_data.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == market_key:
                    for outcome in market["outcomes"]:
                        all_props.append({
                            "player": outcome["name"],
                            "line": outcome["point"],
                            "team_1": home,
                            "team_2": away,
                            "bookmaker": bookmaker["title"]
                        })

    return pd.DataFrame(all_props)
