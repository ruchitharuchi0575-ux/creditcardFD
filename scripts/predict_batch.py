from pathlib import Path
import joblib
import pandas as pd
from sqlalchemy import create_engine

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
MODEL_PATH = BASE_DIR / "models" / "xgboost_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "scaler.joblib"

engine = create_engine(f"sqlite:///{DB_PATH}")


def run_batch_predictions():
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise FileNotFoundError(
            "Model files not found! Run scripts/train_model.py first."
        )

    # Load artifacts and view data
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    print(" Loading features from SQLite for batch scoring...")
    df = pd.read_sql("SELECT * FROM v_fraud_engineered_features", engine)
    df_clean = df.fillna(0)

    features = [
        "Amount",
        "seconds_since_last_txn",
        "rolling_avg_7d_amount",
        "user_spend_rank",
        "amount_to_rolling_avg_ratio",
    ]

    # Batch Predict
    X_scaled = scaler.transform(df_clean[features])
    df["predicted_fraud"] = model.predict(X_scaled)
    df["fraud_probability"] = model.predict_proba(X_scaled)[:, 1]

    # Assign Risk Categories
    def assign_risk(prob):
        if prob >= 0.70:
            return "HIGH RISK"
        elif prob >= 0.35:
            return "MEDIUM RISK"
        return "LOW RISK"

    df["risk_level"] = df["fraud_probability"].apply(assign_risk)

    # Write predictions back to SQLite
    df.to_sql(
        "predicted_fraud_scores", con=engine, if_exists="replace", index=False
    )
    print(
        " Successfully saved batch predictions to SQLite table 'predicted_fraud_scores'!"
    )


if __name__ == "__main__":
    run_batch_predictions()