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
            'first_name': player.get('fn'),
            'last_name': player.get('n'),
            'team_id': player.get('tid'),
            'position': player.get('pos'),
            'market_value': player.get('mv'),
            'prob': player.get('prob'),
            'is_new': player.get('isn')
        })
        
    return result

def get_budget(token, league_id):
    url = f"{BASE_URL}/leagues/{league_id}/me/budget"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    print(data)