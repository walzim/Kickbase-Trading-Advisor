from kickbase_api.get_player_data import login, get_player_market_value, get_player_id, get_player_performance
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import pandas as pd

def main():
    # Load environment variables from .env file
    load_dotenv() 
    USERNAME = os.getenv('KICK_USER')
    PASSWORD = os.getenv('KICK_PASS')

    # Login and get token
    token = login(USERNAME, PASSWORD)
    print("Logged in. Token:", token)

    # we need competition_id, player_id, timeframe
    competition_id = 1 # 1 is for Bundesliga, info from github issue thread
    last_mv_values = 365 # in days, max 365
    last_pfm_values = 50 # in matchdays
    player_name = "Waldemar Anton" 

    # Get player ID
    player_id = get_player_id(token, competition_id, player_name)

    # Get player market value
    market_value = get_player_market_value(token, competition_id, player_id, last_mv_values)

    # Get player performance
    performance = get_player_performance(token, competition_id, player_id, last_pfm_values)

    # Convert to DataFrames
    mv_df = pd.DataFrame(market_value)
    p_df = pd.DataFrame(performance)

    # Filter out p=None
    p_df = p_df[p_df['p'].notna()]

    # Merge on 'md'
    merged_df = pd.merge(p_df, mv_df, on='md', how='inner')

    print(merged_df)

if __name__ == "__main__":
    main()