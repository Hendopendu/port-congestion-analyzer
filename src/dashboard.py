import streamlit as st
import pandas as pd
import os
import plotly.express as px

# 1. Setup Page
st.set_page_config(page_title="Port Congestion Analyzer", layout="wide")
st.title("🚢 Port Congestion & Freight Rate Analyzer")

# 2. Load Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "aligned.csv")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])

    # 3. Sidebar Stats
    st.sidebar.header("Key Metrics")
    st.sidebar.metric("Days of Data", len(df))
    st.sidebar.metric("Avg Ship Count", int(df['Ship_Count'].mean()))
    st.sidebar.metric("Avg Freight Rate", f"${int(df['Index Value'].mean())}")

    # 4. Main Chart
    st.subheader("Visual Correlation: Ships vs. Price")
    
    # Create a chart with two Y-axes
    fig = px.line(df, x='Date', y=['Ship_Count', 'Index Value'], 
                  title="Ship Counts (Congestion) and Freight Rates over Time",
                  labels={"value": "Count / Price", "variable": "Metric"})
    
    st.plotly_chart(fig, use_container_width=True)

    # 5. Data Table
    st.subheader("Raw Aligned Data")
    st.dataframe(df)

else:
    st.error("No aligned data found. Please run the pipeline scripts first!")