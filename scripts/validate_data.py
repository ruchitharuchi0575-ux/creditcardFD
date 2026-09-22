import sys
from pathlib import Path
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "cleaned_transactions.csv"

class TransactionSchema(BaseModel):
    user_id: int
    Amount: float = Field(
        ge=0, description="Transaction amount cannot be negative"
    )
    Class: int = Field(
        ge=0, le=1, description="Class must be 0 (Legit) or 1 (Fraud)"
    )

def validate_dataset():
    print("[INFO] Running Data Quality & Schema Validation...")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing input dataset at {CSV_PATH}")

    # Read CSV with fallback for malformed rows
    try:
        df = pd.read_csv(CSV_PATH, on_bad_lines='skip', engine='python')
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

    errors = 0

    for idx, row in df.iterrows():
        try:
            TransactionSchema(
                user_id=int(row["user_id"]),
                Amount=float(row["Amount"]),
                Class=int(row["Class"])
            )
        except (ValidationError, KeyError, ValueError) as e:
            print(f"[ERROR] Row {idx} Failed Validation: {e}")
            errors += 1

    if errors == 0:
        print(
            f"[SUCCESS] Data Validation Passed Successfully! ({len(df)} rows verified)"
        )
        return True
    else:
        raise ValueError(f"Data Validation Failed with {errors} errors.")

if __name__ == "__main__":
    validate_dataset()