from kickbase_api.constants import BASE_URL
import requests

def get_all_teams(token, competition_id):
    url = f"{BASE_URL}/competitions/{competition_id}/table"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    teams = [
        {
            "team_id": item.get("tid"),   # Team-ID
            "team_name": item.get("tn")   # Team Name
        }
        for item in data.get("it", [])
    ]

    return teams