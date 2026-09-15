from pathlib import Path
import joblib
from imblearn.over_sampling import SMOTE
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine
from xgboost import XGBClassifier

# Path Configurations
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")


def train_model():
    print(" Loading engineered features from SQLite database...")
    df = pd.read_sql("SELECT * FROM v_fraud_engineered_features", engine)
    df = df.fillna(0)

    # Feature & Target Selection
    features = [
        "Amount",
        "seconds_since_last_txn",
        "rolling_avg_7d_amount",
        "user_spend_rank",
        "amount_to_rolling_avg_ratio",
    ]
    target = "Class"

    X = df[features]
    y = df[target]

    # Check class distribution
    fraud_count = y.sum()
    print(
        f" Total records: {len(df)} | Fraud cases: {fraud_count} | Legit cases: {len(df) - fraud_count}"
    )

    # Stratified Train-Test Split (use non-stratified if fraud count is extremely small)
    stratify_option = y if fraud_count >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify_option
    )

    # Scale Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Dynamic SMOTE execution
    train_fraud_count = y_train.sum()

    if train_fraud_count > 1:
        # Dynamically set k_neighbors to be smaller than the available fraud samples
        k_neighbors = min(5, train_fraud_count - 1)
        print(
            f"⚖️ Applying SMOTE with k_neighbors={k_neighbors} for {train_fraud_count} fraud training samples..."
        )
        smote = SMOTE(k_neighbors=k_neighbors, random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
    else:
        print(
            "⚠️ Not enough fraud samples in training set for SMOTE. Training directly on un-sampled data..."
        )
        X_train_res, y_train_res = X_train_scaled, y_train

    # Train XGBoost Classifier
    print("🤖 Training XGBoost Model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.05,
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(X_train_res, y_train_res)

    # Evaluation
    y_pred = model.predict(X_test_scaled)

    # Handle single class case for ROC-AUC
    if len(set(y_test)) > 1:
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
        auc = f"{roc_auc_score(y_test, y_proba):.4f}"
    else:
        auc = "N/A (Only 1 class present in test set)"

    print("\n--- 📊 MODEL PERFORMANCE REPORT ---")
    print(classification_report(y_test, y_pred, zero_division=0))
    print(f"ROC-AUC Score: {auc}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save Artifacts
    joblib.dump(model, MODEL_DIR / "xgboost_model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    print(f"\n Artifacts saved to: {MODEL_DIR}")


if __name__ == "__main__":
    train_model()