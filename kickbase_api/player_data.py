from kickbase_api.constants import BASE_URL
from kickbase_api.team_data import get_all_teams
from datetime import datetime, timedelta
import requests

def get_player_id(token, competition_id, name):
    url = f"{BASE_URL}/competitions/{competition_id}/players/search?query={name}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    player_id = data["it"][0]["pi"]  # Gets first player's ID directly, assuming the search returns only one result

    return player_id

def get_player_market_value(token, competition_id, player_id, last_mv_values):
    timeframe = 365  # amount of last values to retrieve, min 92, max 365
    url = f"{BASE_URL}/competitions/{competition_id}/players/{player_id}/marketvalue/{timeframe}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # get last last_mv_values market values
    market_values = [(item['dt'], item['mv']) for item in data['it'][-last_mv_values:]]

    # convert Unix epoch days to ISO date and wrap in dict
    epoch = datetime(1970, 1, 1)  # Unix epoch
    market_values = [
        {
            "mv": value,
            "md": (epoch + timedelta(days=days)).date().isoformat()
        }
        for days, value in market_values
    ]

    return market_values

def get_player_info(token, competition_id, player_id):
    url = f"{BASE_URL}/competitions/{competition_id}/players/{player_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    player_info = {
        "player_id": data.get("i"),     # Spieler-ID
        "team_id": data.get("tid"),     # Team-ID
        "team_name": data.get("tn"),    # Team Name
        "first_name": data.get("fn"),   # Name
        "last_name": data.get("ln"),    # Last Name
        "position": data.get("pos")     # Position
    }

    return player_info

def get_all_players(token, competition_id):
    all_players = []  # Initialize an empty list to store all players

    team_ids = [team["team_id"] for team in get_all_teams(token, competition_id)]

    for team_id in team_ids:
        url = f"{BASE_URL}/competitions/{competition_id}/teams/{team_id}/teamprofile"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        # Extract player IDs and names
        players = [(player["i"]) for player in data['it']]

        # Append the players to the main list
        all_players.extend(players)

    return all_players  # Return the combined list at the end


def get_player_performance(token, competition_id, player_id, last_pfm_values, player_team):
    url = f"{BASE_URL}/competitions/{competition_id}/players/{player_id}/performance"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # Gather all performance entries
    all_ph = [
        m
        for item in data["it"]
        for m in item["ph"]
    ]

    # Only include performances up to the current date
    current_date = datetime.now().date()
    all_ph = [
        m for m in all_ph
        if datetime.fromisoformat(m["md"].replace("Z", "+00:00")).date() <= current_date
    ]

    # Last n performance values
    performance_values = all_ph[-last_pfm_values:]

    result = []
    for m in performance_values:
        # Extract minutes played, handling possible formats and missing values
        mp_str = m.get("mp", "0'")
        try:
            minutes_played = int(mp_str.replace("'", "")) if mp_str else 0
        except ValueError:
            minutes_played = 0

        # Points
        points = m.get("p", None)

        # Points per Minute
        ppm = points / minutes_played if points is not None and minutes_played > 0 else None

        # Determine match result for player's team
        t1 = m.get("t1")
        t2 = m.get("t2")
        t1g = m.get("t1g")
        t2g = m.get("t2g")
        won = None
        if t1g is not None and t2g is not None:
            if player_team == t1:
                if t1g > t2g:
                    won = 1
                elif t1g < t2g:
                    won = 0
                else:
                    won = None
            elif player_team == t2:
                if t2g > t1g:
                    won = 1
                elif t2g < t1g:
                    won = 0
                else:
                    won = None

        result.append({
            "md": datetime.fromisoformat(m["md"].replace("Z", "+00:00")).date().isoformat(),
            "p": points,
            "mp": minutes_played,
            "ppm": ppm,
            "t1": t1,
            "t2": t2,
            "t1g": t1g,
            "t2g": t2g,
            "won": won,
            "k": m.get("k")
        })

    return result