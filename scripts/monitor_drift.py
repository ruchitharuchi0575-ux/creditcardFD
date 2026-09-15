from pathlib import Path
import pandas as pd
from scipy.stats import ks_2samp
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def check_feature_drift():
    print("📊 Monitoring Feature Drift on SQL Views...")

    df = pd.read_sql("SELECT * FROM v_fraud_engineered_features", engine)

    # Simulating Baseline (First Half) vs Current Data (Second Half)
    midpoint = len(df) // 2
    baseline = df.iloc[:midpoint]
    current = df.iloc[midpoint:]

    features_to_check = [
        "Amount",
        "rolling_avg_7d_amount",
        "amount_to_rolling_avg_ratio",
    ]

    print("\n---  FEATURE DRIFT REPORT (KS-Test) ---")
    for col in features_to_check:
        stat, p_value = ks_2samp(baseline[col].dropna(), current[col].dropna())
        drift_detected = p_value < 0.05  # 5% Significance Threshold

        status = " DRIFT DETECTED" if drift_detected else " STABLE"
        print(f"Feature: {col:<30} | p-value: {p_value:.4f} | Status: {status}")


if __name__ == "__main__":
    check_feature_drift()