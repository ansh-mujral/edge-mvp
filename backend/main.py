from fastapi import FastAPI
from features.matchup_context import add_matchup_context
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "EdgeStack API is live 🔥"}



fantasy_df = pd.read_csv("data/FantasyPros_Fantasy_Football_Points_RB_HALF_2023.csv")
schedule_df = pd.read_csv("data/schedule_2023.csv")
def_rank_df = pd.read_csv("data/FantasyPros_Fantasy_Football_Points_Allowed_2023.csv")

final_df = add_matchup_context(fantasy_df, schedule_df, def_rank_df)
