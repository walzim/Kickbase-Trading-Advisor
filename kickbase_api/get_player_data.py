from datetime import datetime, timedelta
import requests

BASE_URL = "https://api.kickbase.com"

def login(username, password):
    url = f"{BASE_URL}/v4/user/login"
    payload = {
        "em": username,
        "pass": password,
        "loy": False,
        "rep": {}
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("tkn")
    return token

def get_player_market_value(token, competition_id, player_id, last_mv_values):
    timeframe = 92  # amount of last values to retrieve, min 92, max 365 (idk why)
    url = f"{BASE_URL}/v4/competitions/{competition_id}/players/{player_id}/marketvalue/{timeframe}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # get last last_mv_values market values
    market_values = [(item['dt'], item['mv']) for item in data['it'][-last_mv_values:]]

    # dt is the value from unix epoch, who tf thought this was user friendly?
    epoch = datetime(1970, 1, 1)  # Unix epoch
    market_values = [((epoch + timedelta(days=days)).date(), value) for days, value in market_values]

    return market_values

def get_player_id(token, competition_id, name):
    url = f"{BASE_URL}/v4/competitions/{competition_id}/players/search?query={name}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    player_id = data["it"][0]["pi"]  # Gets first player's ID directly, assuming the search returns only one result

    return player_id

def get_player_performacne():
    pass