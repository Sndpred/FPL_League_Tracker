# FPL_League_Tracker
An application that automates the collection, processing, and display of Fantasy Premier League (FPL) data for a private league. It features a scheduled data pipeline, a PostgreSQL database, and a dynamic web interface to showcase league standings, gameweek winners, and a live countdown to the next deadline.


## Project Overview

"The Amazing Battle of FPL" is a full-stack web application designed to track and visualize data for a private Fantasy Premier League (FPL) competition. The project automates the entire process, from fetching the latest FPL data to updating a public-facing website with league standings and gameweek winners.

This application is built for FPL private leagues and provides a central hub for members to view updated standings and key information without manually checking the FPL website.

## Features

- **Automated Data Pipeline**: A scheduled set of Python scripts fetches raw league data from the official FPL API, processes it, and loads it into a PostgreSQL database.
- **Dynamic Leaderboards**: The web interface displays real-time standings for both Classic and Head-to-Head leagues, with data pulled directly from the database.
- **Gameweek Winners**: The application automatically identifies the top-scoring manager each gameweek and displays them on the site. A pop-up congratulates the latest winner.
- **Live Countdown Timer**: A live countdown shows the time remaining until the next FPL deadline, keeping managers on track.
- **Technology Stack**: Built using a modern and efficient stack:
    - **Backend**: Python, Flask
    - **Database**: PostgreSQL (`psycopg2`)
    - **Data Processing**: `pandas`, Requests
    - **Web Server**: Gunicorn
    - **Frontend**: HTML, CSS, JavaScript

## Project Structure
FPL countdown/
├── app.py                      # Main Flask application to run the web server
├── requirements.txt            # Python dependencies
├── Procfile                    # Used by hosting platforms to define the web process
├── data/
│   ├── processed/
│   │   ├── classic_league.csv  # Processed classic league data
│   │   └── h2h_league.csv      # Processed H2H league data
│   └── raw/
│       └── ...                 # Raw JSON data from FPL API fetches
├── scripts/
│   ├── fetch_leagues.py        # Fetches raw data from FPL API
│   ├── process_leagues.py      # Cleans and processes raw data into CSVs
│   ├── insert_processed_data.py# Inserts processed data into the database
│   ├── create_tables.py        # Database schema script
│   └── ...
└── templates/
└── index.html              # Frontend template for the web page


## How to Run Locally

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
    python scripts/fetch_leagues.py
    python scripts/process_leagues.py
    python scripts/insert_processed_data.py
    ```

5.  **Start the Flask Application**:
    ```bash
    flask run
    ```
    (Note: You may need to specify a `FLASK_APP` environment variable: `export FLASK_APP=app.py`)

## Deployment (Free Option)

This project can be deployed for free on cloud platforms that offer a free tier for both a Python web service and a PostgreSQL database, such as **Render**. The project is pre-configured with a `Procfile` for easy deployment.

1.  **Create a Render account** and connect your GitHub repository.
2.  **Create a PostgreSQL database** on Render's free tier.
3.  **Create a Web Service** for your Flask app, connecting it to your repository and setting up the environment variables for your database credentials.
4.  **Set up a Cron Job** on Render to automate the data pipeline scripts (`fetch_leagues.py`, `process_leagues.py`, and `insert_processed_data.py`) to run on a regular schedule.
