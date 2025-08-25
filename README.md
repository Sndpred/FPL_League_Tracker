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


 
**Prerequisites**
- Python 3.x
- PostgreSQL


**Installation**
- Clone this repository to the local machine.
- Navigate to the project directory and install the required Python libraries using pip:
pip install -r requirements.txt

**Local Usage**

Follow these steps to set up and run the application:

1. **Create Database Tables:** Run the create_tables.py script to set up the necessary tables in your PostgreSQL database.
   python scripts/create_tables.py
   
   This script will create tables for the classic league, h2h league, gameweek winners, and FPL deadlines.

2. **Fetch Raw Data:** Run the fetch_leagues.py script to pull the latest league data from the official FPL API.
   python scripts/fetch_leagues.py

3. **Process Data:** Execute the process_leagues.py script to clean and process the raw JSON files into a structured format (CSV files).
   python scripts/process_leagues.py

4. **Insert Data into Database:** Run the insert_processed_data.py script to populate the PostgreSQL database with the processed data.
   python scripts/insert_processed_data.py

5. **Run the Web Application:** Start the Flask server by running the app.py file.
   python app.py
   
   The application will be accessible at http://127.0.0.1:5000/



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





