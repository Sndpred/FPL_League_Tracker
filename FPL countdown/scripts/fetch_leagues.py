import requests
import json
from datetime import datetime
import os

# Ensure the data/raw folder exists
os.makedirs('data/raw', exist_ok=True)

# List of leagues with their type
leagues = [
    {"id": 1653859, "type": "classic"},  # Classic League
    {"id": 1654002, "type": "h2h"}       # H2H League
]

def fetch_league_standings(league_id, league_type='classic'):
    url = f'https://fantasy.premierleague.com/api/leagues-{league_type}/{league_id}/standings/'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

for league in leagues:
    league_id = league['id']
    league_type = league['type']
    print(f'Fetching league {league_id} ({league_type})...')

    try:
        league_data = fetch_league_standings(league_id, league_type)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/raw/league_{league_id}_{timestamp}.json'

        with open(filename, 'w') as f:
            json.dump(league_data, f, indent=4)

        print(f'✅ Saved: {filename}')

    except requests.exceptions.HTTPError as e:
        print(f'❌ Failed to fetch league {league_id} ({league_type}): {e}')
