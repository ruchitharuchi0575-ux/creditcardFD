from pathlib import Path
import pandas as pd
import pytest
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
CSV_PATH = BASE_DIR / "data" / "cleaned_transactions.csv"


@pytest.fixture
def db_engine():
    """Fixture to connect to the SQLite database."""
    return create_engine(f"sqlite:///{DB_PATH}")


def test_cleaned_csv_exists():
    """Ensure the cleaned transactions CSV file exists and is not empty."""
    assert CSV_PATH.exists(), f"Cleaned CSV file not found at {CSV_PATH}"
    df = pd.read_csv(CSV_PATH)
    assert len(df) > 0, "Cleaned CSV file is empty!"


def test_transactions_table_exists(db_engine):
    """Verify that the 'transactions' table was created in SQLite."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'"
    result = pd.read_sql(query, db_engine)
    assert not result.empty, "Table 'transactions' does not exist in SQLite database!"


def test_transactions_row_count_matches(db_engine):
    """Confirm row count in SQLite matches row count in CSV."""
    df_csv = pd.read_csv(CSV_PATH)
    df_db = pd.read_sql("SELECT COUNT(*) as count FROM transactions", db_engine)
    
    assert len(df_csv) == df_db["count"].iloc[0], (
        f"Row count mismatch! CSV: {len(df_csv)}, Database: {df_db['count'].iloc[0]}"
    )


def test_no_null_transaction_ids(db_engine):
    """Verify primary keys / user IDs contain no NULL values."""
    df = pd.read_sql("SELECT * FROM transactions WHERE user_id IS NULL", db_engine)
    assert len(df) == 0, "Found NULL user_id records in 'transactions' table!"