import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONGESTION_FILE = os.path.join(BASE_DIR, "data", "processed", "congestion.csv")
RATES_FILE = os.path.join(BASE_DIR, "data", "processed", "freight_rates.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "aligned.csv")

def align_data():
    if not os.path.exists(CONGESTION_FILE) or not os.path.exists(RATES_FILE):
        print("❌ Processed files missing. Run loader and calculator first!")
        return

    # Load
    df_c = pd.read_csv(CONGESTION_FILE)
    df_r = pd.read_csv(RATES_FILE)

    # NORMALIZE: Force both to be datetime objects and strip time (keep only YYYY-MM-DD)
    df_c['Date'] = pd.to_datetime(df_c['Date']).dt.normalize()
    df_r['Date'] = pd.to_datetime(df_r['Date']).dt.normalize()

    # Merge
    merged = pd.merge(df_c, df_r, on='Date', how='inner')

    if merged.empty:
        print("❌ Still no overlap! Check if your dates in both CSVs actually match.")
    else:
        merged.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Success! Aligned file created with {len(merged)} rows.")
        print(merged.head())

if __name__ == "__main__":
    align_data()