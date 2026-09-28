import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Credit Card Fraud Dashboard", layout="wide")

st.title("Credit Card Fraud Intelligence Dashboard")

# Load Database Data
@st.cache_data(ttl=10)
def load_data():
    if not os.path.exists("data/fraud_predictions.db"):
        return pd.DataFrame()
    
    conn = sqlite3.connect("data/fraud_predictions.db")
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df

df = load_data()

if not df.empty:
    # Top Metrics KPI Bar
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("High Risk Flagged", len(df[df['risk_level'] == 'HIGH RISK']))
    col3.metric("Low Risk Flagged", len(df[df['risk_level'] == 'LOW RISK']))

    st.markdown("---")

    # --- VISUALIZATION GRAPHS SECTION ---
    st.subheader("📊 Analytics & Risk Visualizations")
    
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.write("### Risk Distribution Breakdown")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="risk_level", palette=["#2ecc71", "#e74c3c"], ax=ax1)
        ax1.set_title("Low Risk vs High Risk Fraud Counts")
        ax1.set_ylabel("Transaction Count")
        ax1.set_xlabel("Risk Classification")
        st.pyplot(fig1)  # <-- Renders matplotlib figure directly into Streamlit UI

    with fig_col2:
        st.write("### Fraud Probability Distribution")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.histplot(df["fraud_probability"], bins=15, kde=True, color="#3498db", ax=ax2)
        ax2.set_title("Model Risk Probability Density")
        ax2.set_xlabel("Fraud Probability")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)  # <-- Renders matplotlib figure directly into Streamlit UI

    st.markdown("---")

    # Table & Download CSV Section
    st.subheader("High Risk Fraud Flagged by ML Model")
    high_risk_df = df[df['risk_level'] == 'HIGH RISK']
    st.dataframe(high_risk_df, use_container_width=True)

    csv = high_risk_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download High Risk Report (CSV)",
        data=csv,
        file_name="high_risk_predictions.csv",
        mime="text/csv"
    )

else:
    st.warning("No transaction data found in database. Please run 'python scripts/run_pipeline.py' first.")