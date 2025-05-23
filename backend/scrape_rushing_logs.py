import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_rushing_game_logs(season=2023):
    url = f"https://www.pro-football-reference.com/years/{season}/rushing.htm"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"Failed to fetch data: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"id": "rushing"})

    df = pd.read_html(str(table), header=1)[0]

    # Drop rows where Player == 'Player' (duplicate headers in table body)
    df = df[df["Player"] != "Player"]

    # Flatten column names
    df.columns = [col if not isinstance(col, tuple) else col[1] for col in df.columns]

    # Clean player names
    df['Player'] = df['Player'].str.replace(r"[*+]", "", regex=True)

    return df[["Player", "Team", "Att", "Yds", "TD", "Fmb", "G", "Y/A", "Y/G"]]

if __name__ == "__main__":
    for season in [2023, 2024]:
        print(f"📊 Scraping rushing stats for {season}...")
        df = scrape_rushing_game_logs(season)
        out_path = f"backend/data/rushing_totals_{season}.csv"
        df.to_csv(out_path, index=False)
        print(f"✅ Saved: {out_path}")
