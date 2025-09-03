from kickbase_api.constants import BASE_URL
import requests

def login(username, password):
    url = f"{BASE_URL}/user/login"
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

def get_players_in_squad(token, league_id):
    url = f"{BASE_URL}/leagues/{league_id}/squad"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    return data