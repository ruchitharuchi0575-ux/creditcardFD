import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_CSV_PATH = BASE_DIR / "data" / "cleaned_transactions.csv"
DB_PATH = BASE_DIR / "data" / "fraud_db.db"

def load_to_sql(csv_path):
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        raise ValueError(f"The file {csv_path} is empty! Please run data_cleaning.py first.")
    
    # Load cleaned CSV data
    df = pd.read_csv(csv_path)
    
    # Establish SQLite Engine
    engine = create_engine(f"sqlite:///{DB_PATH}")
    
    # Save to SQLite table 'transactions'
    df.to_sql("transactions", con=engine, if_exists="replace", index=False)
    print(f" Successfully loaded {len(df)} rows into 'transactions' table in: {DB_PATH}")

if __name__ == "__main__":
    load_to_sql(CLEANED_CSV_PATH)