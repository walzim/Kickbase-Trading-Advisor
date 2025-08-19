from kickbase_api.get_player_data import login, get_player_market_value, get_player_id
from dotenv import load_dotenv
import os

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
    last_mv_values = 7 # in days
    player_name = "Waldemar Anton" 

    player_id = get_player_id(token, competition_id, player_name)
    market_value = get_player_market_value(token, competition_id, player_id, last_mv_values)

    print(market_value)
    
if __name__ == "__main__":
    main()