import pandas as pd
from features.matchup_context import add_matchup_context

# Load the necessary CSVs
fantasy_df = pd.read_csv("backend/data/fantasy_rb_weekly_long_2023.csv")
schedule_df = pd.read_csv("backend/data/schedule_2023.csv")
def_rank_df = pd.read_csv("backend/data/FantasyPros_Fantasy_Football_Points_Allowed_2023.csv")

# Add matchup features
result = add_matchup_context(fantasy_df, schedule_df, def_rank_df, season=2023)

# Save or preview the result
result.to_csv("backend/data/fantasy_rb_with_matchups_2023.csv", index=False)
print(result.head(8))
print("✅ File saved: data/fantasy_rb_with_matchups_2023.csv")
