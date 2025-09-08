from kickbase_api.constants import BASE_URL
from datetime import datetime
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

def get_matchdays(token, competition_id):
    url = f"{BASE_URL}/competitions/{competition_id}/matchdays"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    matches = [
        {
            "day": match.get("day"),
            "date": match.get("dt")
        }
        for item in data.get("it", [])
        for match in item.get("it", [])
    ]

    max_dates_per_day = {}
    for m in matches:
        day = m["day"]
        date = datetime.fromisoformat(m["date"].replace("Z", "+00:00"))  # ISO -> datetime
        if day not in max_dates_per_day or date > max_dates_per_day[day]:
            max_dates_per_day[day] = date

    result = [{"day": day, "date": max_dates_per_day[day].isoformat()} for day in sorted(max_dates_per_day)]

    return result