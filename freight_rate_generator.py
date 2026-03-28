import pandas as pd
import numpy as np
import sqlite3
import os

# Paths
DB_PATH = "data/raw/ais_raw.db"
FREIGHT_FILE = "data/raw/fbx_historical.csv"

def seed_everything():
    os.makedirs("data/raw", exist_ok=True)
    
    # 1. Generate 100 days of dates
    dates = pd.date_range(end=pd.Timestamp.now().normalize(), periods=100)

    # 2. Generate and Save Mock Freight Rates
    prices = np.random.randint(2500, 5500, size=100)
    df_freight = pd.DataFrame({'Date': dates, 'Index Value': prices})
    df_freight.to_csv(FREIGHT_FILE, index=False)
    print(f"✅ Created 100 days of Freight Rates in {FREIGHT_FILE}")

    # 3. Seed the SQLite Database with Historical Ships
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clean old data so we start fresh
    cursor.execute("DELETE FROM ship_positions")
    
    print("⏳ Seeding database with historical ship pings...")
    for d in dates:
        # For each day, generate a random number of ships (between 10 and 30)
        num_ships = np.random.randint(10, 31)
        for i in range(num_ships):
            mmsi = f"999{np.random.randint(1000, 9999)}"
            # Insert the ping with the historical date
            cursor.execute(
                "INSERT INTO ship_positions (mmsi, ship_name, lat, lon, timestamp) VALUES (?, ?, ?, ?, ?)",
                (mmsi, f"MockShip_{i}", 1.28, 103.85, d.strftime('%Y-%m-%d %H:%M:%S'))
            )
    
    conn.commit()
    conn.close()
    print(f"✅ Database seeded with 100 days of historical ship traffic.")

if __name__ == "__main__":
    seed_everything()