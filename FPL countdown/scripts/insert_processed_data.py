import pandas as pd
import psycopg2
from datetime import datetime
import requests
import os

# -------------------------------
# Database connection parameters
# -------------------------------
db_params = {
    "host": "localhost",
    "port": 5434,
    "database": "fpl_data",
    "user": "fpl_user",
    "password": "H0grider?"
}

# -------------------------------
# Functions
# -------------------------------

def connect_db():
    try:
        conn = psycopg2.connect(**db_params)
        print("✅ Connected to the database!")
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        return None

def insert_dataframe(df, table_name, conn, mapping, gameweek=None):
    """Insert DataFrame rows into the database table with column mapping and upsert logic."""
    if df.empty:
        print(f"⚠️ Skipping {table_name}: DataFrame is empty.")
        return
        
    try:
        cur = conn.cursor()
        for _, row in df.iterrows():
            columns = []
            values = []
            for src_col, dest_col in mapping.items():
                if src_col in row:
                    columns.append(dest_col)
                    values.append(row[src_col])
            if gameweek:
                columns.append("gameweek")
                values.append(gameweek)
            
            placeholders = ", ".join(["%s"] * len(values))
            columns_str = ", ".join(columns)
            
            upsert_query = f"""
                INSERT INTO {table_name} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT (position, gameweek) DO UPDATE SET
                manager = EXCLUDED.manager,
                points = EXCLUDED.points,
                updated_at = CURRENT_TIMESTAMP;
            """
            cur.execute(upsert_query, values)
        conn.commit()
        cur.close()
        print(f"✅ {table_name} data inserted/updated.")
    except Exception as e:
        print(f"❌ Error inserting into {table_name}: {e}")
        conn.rollback()

def insert_gameweek_winner(classic_df, conn):
    """Insert the winner of the most recently finished gameweek."""
    if classic_df.empty:
        print("❌ DataFrame is empty. Skipping gameweek winner insertion.")
        return
        
    try:
        cur = conn.cursor()
        
        # Debug: Print the DataFrame columns and sample data
        print("🔍 DEBUG INFO:")
        print(f"   DataFrame columns: {list(classic_df.columns)}")
        print(f"   DataFrame shape: {classic_df.shape}")
        
        if not classic_df.empty:
            print("   Sample data (first row):")
            for col in classic_df.columns:
                print(f"     {col}: {classic_df.iloc[0][col]}")
        
        # Try to get gameweek number from different possible columns
        gameweek_number = None
        possible_gw_columns = ['event', 'gameweek', 'current_event', 'gw']
        
        for col in possible_gw_columns:
            if col in classic_df.columns and not classic_df[col].isna().all():
                gameweek_number = int(classic_df[col].iloc[0])
                print(f"   Found gameweek number {gameweek_number} in column '{col}'")
                break
        
        if gameweek_number is None or gameweek_number <= 0:
            print("⚠️ No valid gameweek number found. Trying to get current gameweek from FPL API...")
            # Try to get current gameweek from FPL API
            try:
                response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
                if response.status_code == 200:
                    data = response.json()
                    events = data.get('events', [])
                    for event in events:
                        if event.get('is_current', False) or (event.get('finished', False) and not event.get('data_checked', False)):
                            gameweek_number = event['id']
                            print(f"   Got current gameweek {gameweek_number} from FPL API")
                            break
                    
                    if gameweek_number is None:
                        # Get the latest finished gameweek
                        finished_events = [e for e in events if e.get('finished', False)]
                        if finished_events:
                            gameweek_number = max(finished_events, key=lambda x: x['id'])['id']
                            print(f"   Got latest finished gameweek {gameweek_number} from FPL API")
            except Exception as api_error:
                print(f"   ❌ Failed to get gameweek from API: {api_error}")
                gameweek_number = 1  # Default fallback
                print(f"   Using fallback gameweek: {gameweek_number}")
        
        # Find the winner (rank/position = 1)
        winner_row = None
        possible_rank_columns = ['rank', 'position', 'pos']
        
        for col in possible_rank_columns:
            if col in classic_df.columns:
                winner_rows = classic_df[classic_df[col] == 1]
                if not winner_rows.empty:
                    winner_row = winner_rows.iloc[0]
                    print(f"   Found winner using column '{col}'")
                    break
        
        if winner_row is None:
            # If no rank column, assume first row is the winner (already sorted)
            winner_row = classic_df.iloc[0]
            print("   No rank column found, using first row as winner")
        
        # Get winner name from possible columns
        winner_name = None
        possible_name_columns = ['manager_name', 'player_name', 'name', 'manager', 'entry_name']
        
        for col in possible_name_columns:
            if col in winner_row.index and pd.notna(winner_row[col]):
                winner_name = str(winner_row[col]).strip()
                print(f"   Found winner name '{winner_name}' in column '{col}'")
                break
        
        # Get winner points from possible columns
        winner_points = None
        possible_points_columns = ['event_total', 'event_points', 'points', 'total_points', 'gw_points']
        
        for col in possible_points_columns:
            if col in winner_row.index and pd.notna(winner_row[col]):
                try:
                    winner_points = int(float(winner_row[col]))
                    print(f"   Found winner points {winner_points} in column '{col}'")
                    break
                except (ValueError, TypeError):
                    continue
        
        # Insert winner if we have valid data
        if gameweek_number and gameweek_number > 0 and winner_name:
            if winner_points is None:
                winner_points = 0  # Default if no points found
            
            print(f"🏆 Inserting gameweek winner: GW{gameweek_number} - {winner_name} ({winner_points} points)")
            
            cur.execute("""
                INSERT INTO gameweek_winners (gameweek, winner, points)
                VALUES (%s, %s, %s)
                ON CONFLICT (gameweek) DO UPDATE SET
                    winner = EXCLUDED.winner,
                    points = EXCLUDED.points
            """, (gameweek_number, winner_name, winner_points))
            conn.commit()
            print("✅ Gameweek winner updated successfully.")
        else:
            print(f"❌ Missing required data for gameweek winner:")
            print(f"   Gameweek: {gameweek_number}")
            print(f"   Winner name: {winner_name}")
            print(f"   Winner points: {winner_points}")
        
        cur.close()
    except Exception as e:
        print(f"❌ Error inserting gameweek winner: {e}")
        print(f"   Exception details: {type(e).__name__}: {str(e)}")
        conn.rollback()

def fetch_fpl_deadlines():
    """Fetch FPL deadlines from API."""
    try:
        r = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        r.raise_for_status()
        events = r.json().get("events", [])
        deadlines = []
        for event in events:
            if not event["finished"]:
                deadlines.append({
                    "gameweek": event["id"],
                    "deadline": datetime.fromisoformat(event["deadline_time"].replace("Z", "+00:00"))
                })
        return deadlines
    except Exception as e:
        print("❌ Error fetching FPL deadlines:", e)
        return []

def insert_deadlines(deadlines, conn):
    """Inserts or updates FPL deadlines in the database."""
    try:
        cur = conn.cursor()
        for d in deadlines:
            cur.execute("""
                INSERT INTO fpl_deadline (gameweek, deadline)
                VALUES (%s, %s)
                ON CONFLICT (gameweek) DO UPDATE SET deadline = EXCLUDED.deadline
            """, (d["gameweek"], d["deadline"]))
        conn.commit()
        cur.close()
        print("✅ FPL deadlines updated.")
    except Exception as e:
        print(f"❌ Error updating deadlines: {e}")
        conn.rollback()

# -------------------------------
# Main
# -------------------------------
def main():
    conn = connect_db()
    if not conn:
        return

    try:
        # Check if CSV files exist
        classic_csv_path = "data/processed/classic_league.csv"
        h2h_csv_path = "data/processed/h2h_league.csv"
        
        if not os.path.exists(classic_csv_path):
            print(f"❌ File not found: {classic_csv_path}")
            print("Please run process_leagues.py first to generate the CSV files.")
            conn.close()
            return
            
        if not os.path.exists(h2h_csv_path):
            print(f"❌ File not found: {h2h_csv_path}")
            print("Please run process_leagues.py first to generate the CSV files.")
            conn.close()
            return

        # Read the CSV files
        classic_df = pd.read_csv(classic_csv_path)
        h2h_df = pd.read_csv(h2h_csv_path)
        
        print(f"📊 Loaded {len(classic_df)} classic league entries")
        print(f"🤝 Loaded {len(h2h_df)} H2H league entries")

        # Determine gameweek - try multiple sources
        gameweek = None
        if "event" in classic_df.columns and not classic_df['event'].empty:
            gameweek = classic_df["event"].iloc[0]
        elif "gameweek" in classic_df.columns and not classic_df['gameweek'].empty:
            gameweek = classic_df["gameweek"].iloc[0]

        print(f"🎯 Processing data for gameweek: {gameweek}")

        # Define column mappings
        classic_mapping = {
            "manager_name": "manager",
            "total_points": "points",
            "rank": "position"
        }
        h2h_mapping = {
            "player_name": "manager",
            "points": "points",
            "rank": "position"
        }

        # Insert the data
        insert_dataframe(classic_df, "classic_league", conn, classic_mapping, gameweek)
        insert_dataframe(h2h_df, "h2h_league", conn, h2h_mapping, gameweek)

        # Insert gameweek winner
        insert_gameweek_winner(classic_df, conn)

        # Update deadlines
        deadlines = fetch_fpl_deadlines()
        insert_deadlines(deadlines, conn)

        conn.close()
        print("✅ All operations completed!")

    except Exception as e:
        print(f"❌ Error in main: {e}")
        conn.close()

if __name__ == "__main__":
    main()