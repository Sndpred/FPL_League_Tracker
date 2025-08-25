**FPL_League_Tracker**
An application that automates the collection, processing, and display of Fantasy Premier League (FPL) data for a private league. It features a scheduled data pipeline, a PostgreSQL database, and a dynamic web interface to showcase league standings, gameweek winners, and a live countdown to the next deadline.


**Project Overview**

The application is designed to track and visualize data for a private Fantasy Premier League (FPL) competition. The project automates the entire process, from fetching the latest FPL data to updating a public-facing website with league standings and gameweek winners.

This application is designed for FPL private leagues and serves as a central hub, allowing members to view updated standings and key information without needing to check the FPL website.


**Features**

- **Automated Data Pipeline**: A scheduled set of Python scripts fetches raw league data from the official FPL API, processes it, and loads it into a PostgreSQL database.
- **Dynamic Leaderboards**: The web interface displays real-time standings for both Classic and Head-to-Head leagues, with data pulled directly from the database.
- **Gameweek Winners**: The application automatically identifies the top-scoring managers each gameweek and displays them on the site. A pop-up congratulates the latest winner.
- **Live Countdown Timer**: A live countdown shows the time remaining until the next FPL deadline, keeping managers on track.
- **Technology Stack**: Built using a modern and efficient stack:
    - **Backend**: Python, Flask
    - **Database**: PostgreSQL (`psycopg2`)
    - **Data Processing**: `pandas`, Requests
    - **Web Server**: Gunicorn
    - **Frontend**: HTML, CSS, JavaScript


**How to Run Locally**

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/sndpred/FPL_League_Tracker.git)
    cd FPL-countdown
    ```

2.  **Set up the Database**:
    - Install and run a local PostgreSQL instance (e.g., using Docker or a local installer).
    - Update the `db_params` in `app.py`, `create_tables.py`, and `insert_processed_data.py` with your local database credentials.
    - Run the table creation script: `python scripts/create_tables.py`

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Data Pipeline (Manual Execution)**:
    - Run the scripts in the correct order to populate the database:
    ```bash
    python scripts/create_tables.py
    python scripts/fetch_leagues.py
    python scripts/process_leagues.py
    python scripts/insert_processed_data.py
    ```

5.  **Start the Flask Application**:
    ```bash
    flask run
    ```
    (Note: You may need to specify a `FLASK_APP` environment variable: `export FLASK_APP=app.py`)


**Future Work**
Deploy and set up a cron job to automate the execution of the data pipeline scripts. This project can be deployed for free on cloud platforms that offer a free tier for both a Python web service and a PostgreSQL database, such as **Render**. 

## Project Structure
```text
FPL-countdown/
├── app.py
├── requirements.txt
├── Procfile
├── data/
│   ├── processed/
│   │   ├── classic_league.csv
│   │   └── h2h_league.csv
│   └── raw/
│       └── ...
├── scripts/
│   ├── fetch_leagues.py
│   ├── process_leagues.py
│   ├── insert_processed_data.py
│   ├── create_tables.py
│   └── ...
└── templates/
    └── index.html





