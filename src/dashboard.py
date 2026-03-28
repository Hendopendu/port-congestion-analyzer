import streamlit as st
import pandas as pd
import os
import plotly.express as px
from scipy.stats import pearsonr

# 1. Setup Page
st.set_page_config(page_title="Port Congestion Analyzer", layout="wide")
st.title("🚢 Port Congestion & Freight Rate Analyzer")

# 2. Load Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "aligned.csv")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])

    # --- SIDEBAR STATS ---
    st.sidebar.header("Key Metrics")
    st.sidebar.metric("Days of Data", len(df))
    st.sidebar.metric("Avg Ship Count", int(df['Ship_Count'].mean()))
    st.sidebar.metric("Avg Freight Rate", f"${int(df['Index Value'].mean())}")

    # --- MAIN CHART ---
    st.subheader("Visual Correlation: Ships vs. Price")
    fig = px.line(df, x='Date', y=['Ship_Count', 'Index Value'], 
                  labels={"value": "Count / Price", "variable": "Metric"})
    st.plotly_chart(fig, use_container_width=True)

    # --- NEW: STATISTICAL CORRELATION SECTION ---
    st.divider()
    st.subheader("📊 Statistical Insights (Pearson Correlation)")
    
    # Calculate Standard Correlation
    corr, _ = pearsonr(df['Ship_Count'], df['Index Value'])
    
    # Calculate Lags (7 and 14 days)
    df_7d = df.copy()
    df_7d['Price_Lag_7'] = df_7d['Index Value'].shift(-7)
    df_7d = df_7d.dropna()
    corr_7d, _ = pearsonr(df_7d['Ship_Count'], df_7d['Price_Lag_7']) if len(df_7d) > 1 else (0, 0)

    df_14d = df.copy()
    df_14d['Price_Lag_14'] = df_14d['Index Value'].shift(-14)
    df_14d = df_14d.dropna()
    corr_14d, _ = pearsonr(df_14d['Ship_Count'], df_14d['Price_Lag_14']) if len(df_14d) > 1 else (0, 0)

    # Display in Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Standard Correlation", f"{corr:.2f}")
    col2.metric("7-Day Lag Correlation", f"{corr_7d:.2f}")
    col3.metric("14-Day Lag Correlation", f"{corr_14d:.2f}")

    st.info("""
    **Interpreting the Score ($r$):**
    * **1.0**: Perfect relationship. As ship counts go up, prices go up.
    * **0.0**: No relationship (random).
    * **-1.0**: Inverse relationship.
    """)

    # --- DATA TABLE ---
    st.divider()
    st.subheader("Raw Aligned Data")
    st.dataframe(df)

else:
    st.error("No aligned data found. Please run the pipeline scripts first!")