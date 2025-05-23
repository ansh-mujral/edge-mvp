import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_receiving_totals(season=2023):
    url = f"https://www.pro-football-reference.com/years/{season}/receiving.htm"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"Failed to fetch data: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"id": "receiving"})

    df = pd.read_html(str(table), header=1)[0]
    df = df[df["Player"] != "Player"]

    df.columns = [col if not isinstance(col, tuple) else col[1] for col in df.columns]
    df['Player'] = df['Player'].str.replace(r"[*+]", "", regex=True)

    return df[["Player", "Team", "Tgt", "Rec", "Yds", "TD", "G"]]

if __name__ == "__main__":
    for season in [2023, 2024]:
        print(f"📊 Scraping recieving stats for {season}...")
        df = scrape_receiving_totals(season)
        out_path = f"backend/data/receiving_totals_{season}.csv"
        df.to_csv(out_path, index=False)
        print(f"✅ Saved: {out_path}")
