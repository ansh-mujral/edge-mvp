import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_schedule(season=2023):
    url = f"https://www.pro-football-reference.com/years/{season}/games.htm"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"Failed to fetch schedule for {season}: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"id": "games"})

    df = pd.read_html(str(table), header=0)[0]
    df = df[df["Week"] != "Week"]

    # Rename columns
    df = df.rename(columns={
        "Date": "GameDate",
        "Winner/tie": "Winner",
        "Loser/tie": "Loser",
        "Pts": "WinnerPts", 
        "Unnamed: 5": "Location"
    })

    # Create columns for both teams' points
    df["WinnerPts"] = pd.to_numeric(df["WinnerPts"], errors="coerce")
    df["LoserPts"] = pd.to_numeric(df["Pts.1"], errors="coerce")

    # Identify home/away
    df["HomeTeam"] = df.apply(lambda row: row["Winner"] if row["Location"] != "@" else row["Loser"], axis=1)
    df["AwayTeam"] = df.apply(lambda row: row["Loser"] if row["Location"] != "@" else row["Winner"], axis=1)

    df = df[["Week", "GameDate", "HomeTeam", "AwayTeam", "WinnerPts", "LoserPts"]]

    return df

if __name__ == "__main__":
    for season in [2023, 2024]:
        print(f"📅 Scraping NFL schedule for {season}...")
        df = scrape_schedule(season)
        out_path = f"backend/data/schedule_{season}.csv"
        df.to_csv(out_path, index=False)
        print(f"✅ Saved: {out_path}")
