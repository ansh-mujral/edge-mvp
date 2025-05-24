import pandas as pd

def transform_weekly_fantasy(filepath):
    """
    Convert FantasyPros weekly data (wide format) to long format and remove non-week rows.
    
    Args:
        filepath (str): Path to the original wide-format CSV

    Returns:
        pd.DataFrame: Long-format fantasy data with columns: Player, Team, Week, FantasyPoints
    """
    df = pd.read_csv(filepath)

    # Drop index column if present
    if "#" in df.columns:
        df = df.drop(columns=["#"])

    # Melt weeks into long format
    long_df = df.melt(id_vars=["Player", "Team"], var_name="Week", value_name="FantasyPoints")

    # Keep only numeric weeks
    long_df = long_df[long_df["Week"].str.isnumeric()]

    long_df["Week"] = long_df["Week"].astype(str).str.strip()
    long_df["FantasyPoints"] = pd.to_numeric(long_df["FantasyPoints"], errors="coerce").fillna(0)

    return long_df

# Example usage:
if __name__ == "__main__":
    path = "backend/data/FantasyPros_Fantasy_Football_Points_RB_HALF_2023.csv"
    df_long = transform_weekly_fantasy(path)
    df_long.to_csv("backend/data/fantasy_rb_weekly_long_2023.csv", index=False)
    print("✅ Transformed and saved: data/fantasy_rb_weekly_long_2023.csv")
