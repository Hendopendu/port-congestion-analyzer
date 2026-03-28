import pandas as pd
from scipy.stats import pearsonr
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "aligned.csv")

def run_analysis():
    if not os.path.exists(INPUT_FILE):
        print("❌ Aligned data missing. Run the Aligner first!")
        return

    df = pd.read_csv(INPUT_FILE)
    
    # 1. Basic Correlation (Pearson)
    # This measures how much the two numbers move together (1.0 is perfect, 0 is random)
    corr, _ = pearsonr(df['Ship_Count'], df['Index Value'])
    print(f"📊 Standard Correlation (No Lag): {corr:.4f}")

    # 2. Lagged Correlation (The 'Pro' Analysis)
    # We shift the freight rates back by 7 days to see if today's congestion 
    # predicts prices one week from now.
    for lag in [7, 14, 21]:
        # Shift the price column
        df[f'Price_Lag_{lag}'] = df['Index Value'].shift(-lag)
        
        # We have to drop the empty rows created by the shift
        temp_df = df.dropna(subset=[f'Price_Lag_{lag}'])
        
        lag_corr, _ = pearsonr(temp_df['Ship_Count'], temp_df[f'Price_Lag_{lag}'])
        print(f"🕒 Correlation with {lag}-day Lag: {lag_corr:.4f}")

    print("\n💡 Realist Tip: Since your current data is random (mocked), "
          "these numbers will be close to 0. With real data, you'd look for "
          "the highest number to find the 'reaction time' of the market.")

if __name__ == "__main__":
    run_analysis()