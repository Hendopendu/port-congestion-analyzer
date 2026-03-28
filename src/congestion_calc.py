import sqlite3
import pandas as pd
import os

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "raw", "ais_raw.db")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "congestion.csv")

def calculate_congestion():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    # 1. Connect to our ship database
    conn = sqlite3.connect(DB_PATH)
    
    # 2. SQL Query: Get the date and count unique ships (MMSI)
    # This turns '2026-03-27 14:00:00' into just '2026-03-27'
    query = """
    SELECT date(timestamp) as Date, COUNT(DISTINCT mmsi) as Ship_Count
    FROM ship_positions
    GROUP BY date(timestamp)
    ORDER BY Date ASC
    """
    
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("⚠️ Database is empty! Run your 'ais_ingestor.py' for a few more minutes.")
        return

    # 3. Save to processed folder
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"✅ Success! Congestion calculated for {len(df)} days.")
    print(df.tail()) # Show the latest day's count

if __name__ == "__main__":
    calculate_congestion()