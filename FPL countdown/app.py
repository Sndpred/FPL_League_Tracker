from flask import Flask, render_template
import psycopg2
from datetime import datetime, timezone
import pytz

# DB connection
db_params = {
    "host": "localhost",
    "port": 5434,
    "database": "fpl_data",
    "user": "fpl_user",
    "password": "H0grider?"
}

app = Flask(__name__)

def get_league_standings(table_name):
    """Fetches league standings for a given table name."""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(f"SELECT position, manager, points FROM {table_name} ORDER BY position ASC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def get_gameweek_winners():
    """Fetches all gameweek winners."""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Modified query to include gameweeks >= 1 and order properly
        cur.execute("SELECT gameweek, winner, points FROM gameweek_winners WHERE gameweek >= 1 ORDER BY gameweek ASC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print(f"Fetched gameweek winners: {rows}")  # Debug print
        return rows
    except Exception as e:
        print(f"Error fetching gameweek winners: {e}")
        return []

def get_classic_winner():
    """Fetches the most recent classic league winner for the popup."""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("""
            SELECT gameweek, winner, points
            FROM gameweek_winners
            WHERE gameweek >= 1
            ORDER BY gameweek DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            winner_data = {"gameweek": row[0], "winner": row[1], "points": row[2]}
            print(f"Classic winner data: {winner_data}")  # Debug print
            return winner_data
        else:
            print("No winner data found")  # Debug print
        return None
    except Exception as e:
        print(f"Error fetching classic winner: {e}")
        return None

def get_next_deadline():
    """Fetches the next FPL gameweek deadline."""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("""
            SELECT gameweek, deadline
            FROM fpl_deadline
            WHERE deadline > NOW()
            ORDER BY deadline ASC
            LIMIT 1
        """)
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            est = pytz.timezone('US/Eastern')
            return {"gameweek": row[0], "deadline": row[1].astimezone(est)}
        return None
    except Exception as e:
        print(f"Error fetching next deadline: {e}")
        return None

@app.route("/")
def index():
    classic_table = get_league_standings("classic_league")
    h2h_table = get_league_standings("h2h_league")
    gameweek_winners = get_gameweek_winners()
    next_deadline = get_next_deadline()
    classic_winner = get_classic_winner()
    
    # Debug prints
    print(f"Gameweek winners: {gameweek_winners}")
    print(f"Classic winner: {classic_winner}")
    
    # Hardcoded team members list
    team_members = [
        "Ajit Pradhan", "Arbind Chiluwal", "Bharat Dankoti", "Dhiraj Khanal", 
        "Dipendra Shrestha", "Kobid Panthi", "Prakash Pandey", "Prashant Acharya", 
        "Rojan Malla", "Roshan Shrestha", "Sagar Pandey", "Sandeep Rupakheti", 
        "Sanish Maharjan", "Suresh Chaudhary", "Yogesh Sapkota"
    ]

    return render_template(
        "index.html",
        classic_table=classic_table,
        h2h_table=h2h_table,
        gameweek_winners=gameweek_winners,
        next_deadline=next_deadline,
        winner=classic_winner,
        team_members=team_members
    )

if __name__ == "__main__":
    app.run(debug=True)