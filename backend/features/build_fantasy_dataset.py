import pandas as pd
from nfl_data_py import import_weekly_data

# === Load Defense Data ===
def load_combined_defense_data():
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

    df_2023 = pd.read_csv("backend/data/FantasyPros_Fantasy_Football_Points_Allowed_2023.csv")
    df_2024 = pd.read_csv("backend/data/FantasyPros_Fantasy_Football_Points_Allowed_2024.csv")

    df_2023.columns = df_2023.columns.str.strip()
    df_2024.columns = df_2024.columns.str.strip()

    df_2023["season"] = 2023
    df_2024["season"] = 2024

    df_all = pd.concat([df_2023, df_2024], ignore_index=True)
    df_all["Team_abbr"] = df_all["Team"].map(TEAM_NAME_TO_ABBR)
    df_all = df_all.rename(columns={"Defense (DEF)": "Team_abbr"})
    return df_all

# === Extract relevant position-wise defense columns ===
def create_def_subset(def_all, col, pos_label):
    col_map = {
        "QB": ("QB", "Rank.1"),
        "RB": ("RB", "Rank.2"),
        "WR": ("WR", "Rank.3"),
        "TE": ("TE", "Rank.4")
    }

    if col not in col_map:
        raise ValueError(f"Position {col} is not supported. Must be one of {list(col_map.keys())}.")

    points_col, rank_col = col_map[col]

    # Check columns exist
    if points_col not in def_all.columns or rank_col not in def_all.columns:
        raise ValueError(f"Columns '{points_col}' or '{rank_col}' not found in defense data.")

    return def_all[["Team_abbr", "season", points_col, rank_col]].rename(columns={
        points_col: f"{pos_label}_points_allowed",
        rank_col: f"{pos_label}_rank_allowed"
    })

# === Filter by position, merge with defense data ===
def filter_and_merge(weekly_df, pos, def_df, extra_cols):
    df = weekly_df[weekly_df["position"] == pos].copy()
    df = df[["player_display_name", "recent_team", "week", "season", "opponent_team", "headshot_url",
             "fantasy_points", "fantasy_points_ppr", *extra_cols]]

    df = df.merge(
        def_df,
        left_on=["opponent_team", "season"],
        right_on=["Team_abbr", "season"],
        how="left"
    )
    df.drop(columns=["Team_abbr"], inplace=True)
    return df

# === Main pipeline ===
def enrich_all_positions(seasons):
    weekly_df = import_weekly_data(seasons)
    defense_all = load_combined_defense_data()

    # Defense subsets for positions
    def_rb = create_def_subset(defense_all, "RB", "rb")
    def_wr = create_def_subset(defense_all, "WR", "wr")
    def_te = create_def_subset(defense_all, "TE", "te")
    def_qb = create_def_subset(defense_all, "QB", "qb")

    rb_df = filter_and_merge(weekly_df, "RB", def_rb, ["carries", "rushing_yards", "rushing_tds", "targets", "target_share", "receptions", "receiving_yards", "receiving_tds"])
    wr_df = filter_and_merge(weekly_df, "WR", def_wr, ["targets", "target_share", "receptions", "receiving_yards", "receiving_tds", "air_yards_share", "wopr"])
    te_df = filter_and_merge(weekly_df, "TE", def_te, ["targets", "target_share", "receptions", "receiving_yards", "receiving_tds"])
    qb_df = filter_and_merge(weekly_df, "QB", def_qb, ["completions", "attempts", "passing_yards", "passing_tds", "interceptions", "sacks"])

    # Save each to CSV
    rb_df.to_csv("backend/data/enriched_rb.csv", index=False)
    wr_df.to_csv("backend/data/enriched_wr.csv", index=False)
    te_df.to_csv("backend/data/enriched_te.csv", index=False)
    qb_df.to_csv("backend/data/enriched_qb.csv", index=False)
    print(rb_df.head(3))
    print(wr_df.head(3))
    print(te_df.head(3))
    print(qb_df.head(3))
    print("✅ All enriched position files saved!")

# === Run if script is executed ===
if __name__ == "__main__":
    enrich_all_positions([2023, 2024])
