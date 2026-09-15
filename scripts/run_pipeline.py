import logging
from pathlib import Path
import subprocess
import sys

# Logging Setup
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_and_run(command, step_name):
    print(f"\n🚀 Executing Step: {step_name}...")
    logging.info(f"Starting {step_name}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f" {step_name} completed successfully!")
        logging.info(f"Completed {step_name}")
    else:
        print(f"❌ Error in {step_name}:\n{result.stderr}")
        logging.error(f"Failed {step_name}: {result.stderr}")
        sys.exit(1)


def run_full_pipeline():
    print(" STARTING END-TO-END TIER 4 DATA & ML PIPELINE ")

    # Step 1: Data Cleaning
    log_and_run("python scripts/data_cleaning.py", "Data Cleaning")

    # Step 2: Data Quality & Schema Checks
    log_and_run("python scripts/validate_data.py", "Data Quality Validation")

    # Step 3: SQL Ingestion
    log_and_run("python scripts/sql_ingestion.py", "SQL Data Ingestion")

    # Step 4: SQL Feature Engineering
    log_and_run(
        'python -c "import sqlite3; conn = sqlite3.connect(\'data/fraud_db.db\'); conn.executescript(open(\'scripts/feature_engineering.sql\').read())"',
        "SQL Feature Engineering View Creation",
    )

    # Step 5: Run Unit Tests
    log_and_run("pytest tests/", "Automated Pytest Suite")

    # Step 6: ML Model Training
    log_and_run("python scripts/train_model.py", "XGBoost Model Training")

    # Step 7: Batch Prediction
    log_and_run("python scripts/predict_batch.py", "Batch Fraud Predictions")

    # Step 8: Feature Drift Monitoring
    log_and_run("python scripts/monitor_drift.py", "Feature Drift Check")

    print("\n🎉 ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    run_full_pipeline()