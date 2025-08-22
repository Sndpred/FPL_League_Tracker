#import libraries
import json
import pandas as pd
import glob
from datetime import datetime
import os

#function to load JSON files
def load_json_files(path_pattern):
    """Loads all JSON files matching a pattern into a list of dictionaries."""
    files = glob.glob(path_pattern)
    data_list = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            data_list.append(data)
    return data_list

#extract classic league standings
def extract_classic_standings(league_json):
    """Extracts classic league standings into a DataFrame."""
    standings = league_json['standings']['results']
    rows = []
    current_gameweek = league_json.get('league', {}).get('event_current')
    for player in standings:
        rows.append({
            'manager_name': player['player_name'],
            'entry': player['entry'],
            'total_points': player['total'],
            'rank': player['rank'],
            'event_points': player['event_total'],
            'event': current_gameweek
        })
    return pd.DataFrame(rows)

#extract H2H standings
def extract_h2h_standings(h2h_json):
    """Extracts H2H league standings into a DataFrame."""
    standings = []
    current_gameweek = h2h_json.get('league', {}).get('event_current')
    for player in h2h_json['standings']['results']:
        standings.append({
            'rank': player['rank'],
            'player_name': player['player_name'],
            'points': player['total'],
            'matches_played': player.get('matches', player.get('matches_played', 0)),
            'event': current_gameweek
        })
    return pd.DataFrame(standings)

def main():
    # Ensure the data/processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # Process all JSON files in data/raw
    # Classic league JSON files
    classic_files = 'data/raw/league_1653859_*.json'
    classic_data_list = load_json_files(classic_files)

    classic_dfs = [extract_classic_standings(data) for data in classic_data_list]
    
    if not classic_dfs:
        print("❌ No classic league data found. Please run fetch_leagues.py first.")
        return
        
    classic_df = pd.concat(classic_dfs, ignore_index=True)
    classic_df['league_type'] = 'classic'
    classic_df['timestamp'] = datetime.now()
    
    # Clean data: convert to numeric and fill NaNs
    classic_df['total_points'] = pd.to_numeric(classic_df['total_points'], errors='coerce').fillna(0)
    classic_df['event_points'] = pd.to_numeric(classic_df['event_points'], errors='coerce').fillna(0)
    classic_df['rank'] = pd.to_numeric(classic_df['rank'], errors='coerce').fillna(0)
    classic_df['event'] = pd.to_numeric(classic_df['event'], errors='coerce').fillna(0)
    
    # Drop duplicates to ensure each manager has only one final entry for each gameweek.
    if 'entry' in classic_df.columns and 'event' in classic_df.columns:
        classic_df = classic_df.sort_values('timestamp').drop_duplicates(subset=['entry', 'event'], keep='last')
        
    # H2H league JSON files
    h2h_files = 'data/raw/league_1654002_*.json'
    h2h_data_list = load_json_files(h2h_files)
    
    if not h2h_data_list:
        print("❌ No H2H league data found. Please run fetch_leagues.py first.")
        return
    
    h2h_dfs = [extract_h2h_standings(data) for data in h2h_data_list]
    h2h_df = pd.concat(h2h_dfs, ignore_index=True)
    h2h_df['league_type'] = 'h2h'
    h2h_df['timestamp'] = datetime.now()

    # Clean data: convert to numeric and fill NaNs
    h2h_df['points'] = pd.to_numeric(h2h_df['points'], errors='coerce').fillna(0)
    h2h_df['rank'] = pd.to_numeric(h2h_df['rank'], errors='coerce').fillna(0)
    h2h_df['event'] = pd.to_numeric(h2h_df['event'], errors='coerce').fillna(0)

    if 'player_name' in h2h_df.columns and 'event' in h2h_df.columns:
        h2h_df = h2h_df.sort_values('timestamp').drop_duplicates(subset=['player_name', 'event'], keep='last')
        
    # Save processed data to csv
    classic_df.to_csv('data/processed/classic_league.csv', index=False)
    h2h_df.to_csv('data/processed/h2h_league.csv', index=False)

    print("✅ Processed data saved in 'data/processed/'")

if __name__ == "__main__":
    main()