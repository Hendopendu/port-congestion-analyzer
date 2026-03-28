import pandas as pd
import os

# 1. Setup Paths (Same logic as the Ingestor)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "fbx_historical.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "freight_rates.csv")

def process_freight_data():
    print(f"📂 Looking for: {INPUT_FILE}")
    
    # 2. Check if the file actually exists
    if not os.path.exists(INPUT_FILE):
        print("❌ Error: 'fbx_historical.csv' is missing from data/raw/")
        return

    # 3. Read the CSV using Pandas
    df = pd.read_csv(INPUT_FILE)
    
    # 4. DATA CLEANING (The important part)
    # Ensure the 'Date' column is recognized as actual dates, not just text
    # Note: If your CSV column is named 'date' (lowercase), change it below
    date_col = 'Date' 
    price_col = 'Index Value' # Or 'Price' depending on your file
    
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        
        # Sort by date so our chart looks right later
        df = df.sort_values(by=date_col)

        # Drop any rows that are completely empty
        df = df.dropna(subset=[date_col, price_col])

        # 5. Save to the 'processed' folder
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)
        
        print(f"✅ Success! Processed {len(df)} price points.")
        print(f"💾 Saved to: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Error during cleaning: {e}")
        print("Tip: Check if your CSV column names match 'Date' and 'Index Value'")

if __name__ == "__main__":
    process_freight_data()