from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
SQL_PATH = BASE_DIR / "scripts" / "feature_engineering.sql"


def build_feature_store():
    print("🛠️ Creating feature engineering view in SQLite...")

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"Missing SQL file at {SQL_PATH}")

    # Read SQL script
    with open(SQL_PATH, "r") as f:
        sql_script = f.read()

    # Connect to SQLite and execute
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

    print(
        " Successfully created/updated 'v_fraud_engineered_features' view in fraud_db.db!"
    )


if __name__ == "__main__":
    build_feature_store()