import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine("sqlite:///data/fraud_db.db")

st.title("Credit Card Fraud Intelligence Dashboard (Tier 3)")

# Query predicted scores from SQLite
try:
    df = pd.read_sql("SELECT * FROM predicted_fraud_scores", engine)

    # Key Metrics Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Predicted Fraud Cases", int((df["predicted_fraud"] == 1).sum()))
    col3.metric(
        "High Risk Count", int((df["risk_level"] == "HIGH RISK").sum())
    )

    st.subheader("High Risk Fraud Flagged by ML Model")
    high_risk_df = df[df["risk_level"] == "HIGH RISK"][
        ["user_id", "Amount", "fraud_probability", "risk_level"]
    ]
    st.dataframe(high_risk_df)

except Exception as e:
    st.warning("Please run `scripts/predict_batch.py` to generate ML predictions table.")