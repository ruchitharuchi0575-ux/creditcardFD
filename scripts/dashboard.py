import streamlit as st
import pandas as pd
import sqlite3
import os

# --- SAFE DATABASE INITIALIZATION & QUERY ---
def get_high_risk_data():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect("data/fraud_predictions.db")
    cursor = conn.cursor()
    
    # 1. Create predictions table if it does not exist yet
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
    
    # 2. Safely query high-risk records
    query = "SELECT * FROM predictions WHERE risk_level = 'HIGH RISK'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

# --- DASHBOARD UI ---
st.subheader("High Risk Fraud Flagged by ML Model")

high_risk_df = get_high_risk_data()

if not high_risk_df.empty:
    st.dataframe(high_risk_df)
    
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