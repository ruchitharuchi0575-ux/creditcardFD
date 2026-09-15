from pathlib import Path
import pandas as pd

import pytest
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"


@pytest.fixture
def db_engine():
    return create_engine(f"sqlite:///{DB_PATH}")


def test_transactions_table_not_empty(db_engine):
    df = pd.read_sql("SELECT COUNT(*) as count FROM transactions", db_engine)
    assert df["count"].iloc[0] > 0, "Transactions table should not be empty!"


def test_engineered_view_schema(db_engine):
    df = pd.read_sql(
        "SELECT * FROM v_fraud_engineered_features LIMIT 1", db_engine
    )
    expected_columns = [
        "user_id",
        "Amount",
        "Class",
        "seconds_since_last_txn",
        "rolling_avg_7d_amount",
        "amount_to_rolling_avg_ratio",
    ]

    for col in expected_columns:
        assert col in df.columns, f"Missing required feature column: {col}"


def test_no_negative_amounts(db_engine):
    df = pd.read_sql("SELECT Amount FROM transactions WHERE Amount < 0", db_engine)
    assert len(df) == 0, "Found negative transaction amounts in database!"