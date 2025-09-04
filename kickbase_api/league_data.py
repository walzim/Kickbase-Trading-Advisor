from kickbase_api.constants import BASE_URL
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