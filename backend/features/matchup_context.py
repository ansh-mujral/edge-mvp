import pandas as pd

TEAM_ABBR_TO_NAME = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "JAC": "Jacksonville Jaguars", 
    "KC": "Kansas City Chiefs",
    "LV": "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SEA": "Seattle Seahawks",
    "SF": "San Francisco 49ers",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders"
}

def add_matchup_context(fantasy_df, schedule_df, def_vs_rb_df, season=2023):
    # Standardize columns
    fantasy_df["Week"] = fantasy_df["Week"].astype(str)
    fantasy_df["Team"] = fantasy_df["Team"].map(TEAM_ABBR_TO_NAME)

    schedule_df["Week"] = schedule_df["Week"].astype(str)
    def_vs_rb_df.columns = def_vs_rb_df.columns.str.strip()

    # Melt DEF vs POS so we can map by team + week
    def_vs_rb_df = def_vs_rb_df.rename(columns={"Team": "Opponent"})
    def_vs_rb_df["Opponent"] = def_vs_rb_df["Opponent"].str.strip()

    # Create a team-to-opponent mapping from schedule
    home = schedule_df[["Week", "HomeTeam", "AwayTeam"]].copy()
    away = schedule_df[["Week", "AwayTeam", "HomeTeam"]].copy()

    home.columns = ["Week", "Team", "Opponent"]
    away.columns = ["Week", "Team", "Opponent"]

    matchup_map = pd.concat([home, away])
    matchup_map["Home"] = matchup_map["Team"] == matchup_map["Team"]

    # Merge fantasy data with opponent/team matchup
    merged = pd.merge(fantasy_df, matchup_map, on=["Week", "Team"], how="left")

    # Merge with DEF vs RB rankings
    def_rank_col = [col for col in def_vs_rb_df.columns if "RB" in col][0]
    def_vs_rb_df = def_vs_rb_df[["Opponent", def_rank_col]]
    def_vs_rb_df = def_vs_rb_df.rename(columns={def_rank_col: "DEF_vs_RB_Rank"})

    merged = pd.merge(merged, def_vs_rb_df, on="Opponent", how="left")

    return merged