from pathlib import Path
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "cleaned_transactions.csv"


# Schema Definition
class TransactionSchema(BaseModel):
    user_id: int
    Amount: float = Field(
        ge=0, description="Transaction amount cannot be negative"
    )
    Class: int = Field(
        ge=0, le=1, description="Class must be 0 (Legit) or 1 (Fraud)"
    )


def validate_dataset():
    print("🔍 Running Data Quality & Schema Validation...")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing input dataset at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    errors = 0

    for idx, row in df.iterrows():
        try:
            TransactionSchema(
                user_id=row["user_id"], Amount=row["Amount"], Class=row["Class"]
            )
        except ValidationError as e:
            print(f"❌ Row {idx} Failed Validation: {e}")
            errors += 1

    if errors == 0:
        print(
            f" Data Validation Passed Successfully! ({len(df)} rows verified)"
        )
        return True
    else:
        raise ValueError(f"Data Validation Failed with {errors} errors.")


if __name__ == "__main__":
    validate_dataset()