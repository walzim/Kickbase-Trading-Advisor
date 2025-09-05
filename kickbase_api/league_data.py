from kickbase_api.constants import BASE_URL
import pandas as pd
import requests

def get_leagues_infos(token):
    url = f"{BASE_URL}/leagues/selection"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    result = []

    for item in data.get("it", []):
        result.append({
            "id": item.get("i"),
            "name": item.get("n")
        })

    return result

def get_players_on_market(token, league_id):
    url = f"{BASE_URL}/leagues/{league_id}/market"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    result = []

    for player in data.get('it', []):
        result.append({
            'id': player.get('i'),
            'prob': player.get('prob'),
            "exp": player.get("exs"),
        })

    return result

def get_budget(token, league_id):
    url = f"{BASE_URL}/leagues/{league_id}/me/budget"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    print(data)

def get_league_id(token, league_name):
    league_infos = get_leagues_infos(token)
    selected_league = [league for league in league_infos if league["name"] == league_name]
    league_id = selected_league[0]["id"]

    return league_id

def get_activities(token, league_id):
    # TODO magic number with 1000, have to find a better solution
    # TODO instead of hardcoded date let the user provide it
    url = f"{BASE_URL}/leagues/{league_id}/activitiesFeed?max=5000&query=dt>=2025-08-08"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    login = [entry for entry in data["af"] if entry.get("t") == 22]
    
    achievements = [entry for entry in data["af"] if entry.get("t") == 26]

    trade = [entry for entry in data["af"] if entry.get("t") == 15]
    trading = [
        {k: entry["data"].get(k) for k in ["byr", "slr", "pi", "pn", "tid", "trp"]}
        for entry in trade
        if entry.get("t") == 15
    ]

    return trading, login, achievements

# TODO achievements can be achieved multiple times, have to sum them up
def get_achievement_reward(token, league_id, achievement_id):
    url = f"{BASE_URL}/leagues/{league_id}/user/achievements/{achievement_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    data = data["er"]

    return data

def get_managers(token, league_id):
    url = f"{BASE_URL}/leagues/{league_id}/ranking"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    user_info = [(user["n"], user["i"]) for user in data["us"]]

    return user_info

def get_manager_performance(token, league_id, manager_id, manager_name):
    url = f"{BASE_URL}/leagues/{league_id}/managers/{manager_id}/performance"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    tp_value = data["it"][0]["tp"]  # tp extrahieren

    return {
        "name": manager_name,
        "tp": tp_value
    }