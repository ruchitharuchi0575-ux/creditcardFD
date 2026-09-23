import streamlit as st
import pandas as pd
import sqlite3
import os

# --- MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="Credit Card Fraud Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CACHE DATABASE READS TO REDUCE WEBSOCKET STRAIN ---
@st.cache_data(ttl=10)  # Refreshes every 10 seconds
def get_high_risk_data():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/fraud_predictions.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            Amount REAL,
            fraud_probability REAL,
            risk_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    query = "SELECT * FROM predictions WHERE risk_level = 'HIGH RISK'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- DASHBOARD LAYOUT ---
st.title("Credit Card Fraud Intelligence Dashboard")
st.subheader("High Risk Fraud Flagged by ML Model")

high_risk_df = get_high_risk_data()

if not high_risk_df.empty:
    st.dataframe(high_risk_df, use_container_width=True)
    
    csv_data = high_risk_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download High Risk Report (CSV)",
        data=csv_data,
        file_name="high_risk_fraud_predictions.csv",
        mime="text/csv",
        key="download-high-risk-csv"
    )
else:
    st.info("No high-risk transactions recorded yet.")