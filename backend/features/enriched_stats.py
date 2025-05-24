import pandas as pd
from nfl_data_py import import_weekly_data

TEAM_NAME_TO_ABBR = {
    "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF", "Carolina Panthers": "CAR", "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
    "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR", "Miami Dolphins": "MIA", "Minnesota Vikings": "MIN",
    "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
    "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN", "Washington Commanders": "WAS"
}


def normalize_name(name):
    if pd.isna(name):
        return ""
    return str(name).strip().lower().replace('.', '').replace(',', '')

def enrich_with_game_stats(fantasy_filepath, output_filepath, season=2023):
    # Load existing fantasy data
    fantasy_df = pd.read_csv(fantasy_filepath)
    fantasy_df["Week"] = fantasy_df["Week"].astype(str)

    # Load NFL weekly data
    weekly = import_weekly_data([season])
    print(weekly.columns.tolist())
#     print(weekly[weekly['position'] == 'RB'][[
#     'player_display_name', 'recent_team', 'week',
#     'headshot_url', 
#     'carries', 'rushing_yards', 'rushing_tds',
#     'targets', 'receptions', 'receiving_yards', 'receiving_tds',
#     'fantasy_points', 'fantasy_points_ppr'
# ]].head(8))

    # Filter for RBs and relevant columns
    rb_stats = weekly[weekly['position'] == 'RB'][[
    'player_display_name', 'recent_team', 'week',
    'headshot_url', 
    'carries', 'rushing_yards', 'rushing_tds',
    'targets', 'receptions', 'receiving_yards', 'receiving_tds',
    'fantasy_points', 'fantasy_points_ppr'
    ]].copy()

    # Normalize for merge
    rb_stats.rename(columns={
        'player_display_name': 'Player',
        'recent_team': 'Team',
        'week': 'Week'
    }, inplace=True)
    rb_stats['Week'] = rb_stats['Week'].astype(str)

    fantasy_df['Player_norm'] = fantasy_df['Player'].apply(normalize_name)
    rb_stats['Player_norm'] = rb_stats['Player'].apply(normalize_name)

    fantasy_df['Team_abbr'] = fantasy_df['Team'].map(TEAM_NAME_TO_ABBR)

    fantasy_df['Week'] = fantasy_df['Week'].astype(int)
    rb_stats['Week'] = rb_stats['Week'].astype(int)

    # Merge and save
    merged = pd.merge(
        fantasy_df,
        rb_stats,
        how="left",
        left_on=["Player_norm", "Week"],
        right_on=["Player_norm", "Week"]
    )

    # Save
    merged.to_csv(output_filepath, index=False)
    print(f"✅ Enriched data saved to {output_filepath}")

# If you want to run it directly
if __name__ == "__main__":
    enrich_with_game_stats(
        "backend/data/fantasy_rb_with_matchups_2023.csv",
        "backend/data/fantasy_rb_enriched_2023.csv"
    )
