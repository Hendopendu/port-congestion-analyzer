import asyncio
import json
import os
import sqlite3
from websockets import connect
from dotenv import load_dotenv

# 1. PATH FINDER: This ensures the script finds 'data/raw' even inside Docker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "raw", "ais_raw.db")

load_dotenv()
API_KEY = os.getenv("AISSTREAM_API_KEY")

def init_db():
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ship_positions (
            mmsi TEXT,
            ship_name TEXT,
            lat REAL,
            lon REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    print(f"✅ Database initialized at: {DB_PATH}")
    return conn

async def listen_and_save():
    db_conn = init_db()
    cursor = db_conn.cursor()
    url = "wss://stream.aisstream.io/v0/stream"
    
    async with connect(url) as websocket:
        subscribe_message = {
            "APIKey": API_KEY,
            "BoundingBoxes": [[[1.05, 103.45], [1.45, 104.15]]] # Singapore
        }

        await websocket.send(json.dumps(subscribe_message))
        print("📡 Connected to AISStream...")

        async for message in websocket:
            try:
                data = json.loads(message)
                metadata = data.get("MetaData", {})
                
                ship_name = metadata.get("ShipName", "Unknown")
                mmsi = metadata.get("MMSI")
                lat = metadata.get("latitude")
                lon = metadata.get("longitude")
                
                if lat and lon:
                    cursor.execute(
                        "INSERT INTO ship_positions (mmsi, ship_name, lat, lon) VALUES (?, ?, ?, ?)",
                        (str(mmsi), ship_name, lat, lon)
                    )
                    db_conn.commit()
                    # Using flush=True forces the terminal to show this immediately
                    print(f"💾 SAVED: {ship_name} at {lat}, {lon}", flush=True)
                else:
                    print("⚠️ Received data but missing Lat/Lon", flush=True)
                    
            except Exception as e:
                print(f"❌ Error saving to DB: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(listen_and_save())