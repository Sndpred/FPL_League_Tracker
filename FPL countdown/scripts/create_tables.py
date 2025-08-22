import psycopg2

# Database connection parameters
db_params = {
    "host": "localhost",
    "port": 5434,
    "database": "fpl_data",
    "user": "fpl_user",
    "password": "H0grider?"
}

TABLE_QUERIES = {
    "classic_league": """
        DROP TABLE IF EXISTS classic_league;
        CREATE TABLE classic_league (
            position INT,
            manager VARCHAR(100),
            points INT,
            gameweek INT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT classic_unique UNIQUE (position, gameweek)
        );
    """,
    "h2h_league": """
        DROP TABLE IF EXISTS h2h_league;
        CREATE TABLE h2h_league (
            position INT,
            manager VARCHAR(100),
            points INT,
            gameweek INT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT h2h_unique UNIQUE (position, gameweek)
        );
    """,
    "gameweek_winners": """
        DROP TABLE IF EXISTS gameweek_winners;
        CREATE TABLE gameweek_winners (
            gameweek INT PRIMARY KEY,
            winner VARCHAR(100),
            points INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "fpl_deadline": """
        DROP TABLE IF EXISTS fpl_deadline;
        CREATE TABLE fpl_deadline (
            gameweek INT PRIMARY KEY,
            deadline TIMESTAMP
        );
    """
}

def create_tables():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        print("✅ Connected to the database!")

        for table_name, query in TABLE_QUERIES.items():
            cursor.execute(query)
            print(f"✅ Table '{table_name}' dropped and recreated.")

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All tables are ready!")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    create_tables()