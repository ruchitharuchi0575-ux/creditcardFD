import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = BASE_DIR / "data" / "raw_transactions.csv"
CLEANED_CSV = BASE_DIR / "data" / "cleaned_transactions.csv"

def clean_data():
    if not RAW_CSV.exists():
        # Fallback if raw file doesn't exist
        os.makedirs(BASE_DIR / "data", exist_ok=True)
        df_raw = pd.DataFrame({
            "user_id": range(1000, 1050),
            "Amount": [round(10.0 + i * 2.5, 2) for i in range(50)],
            "Class": [1 if i % 10 == 0 else 0 for i in range(50)]
        })
        df_raw.to_csv(RAW_CSV, index=False)

    # Read raw data and clean
    df = pd.read_csv(RAW_CSV, on_bad_lines='skip')
    
    # Keep only necessary columns for schema validation
    required_cols = ["user_id", "Amount", "Class"]
    available_cols = [c for c in required_cols if c in df.columns]
    
    if len(available_cols) == 3:
        df = df[required_cols]
    
    # Drop nulls & invalid values
    df = df.dropna()
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Class'] = pd.to_numeric(df['Class'], errors='coerce')
    df = df.dropna()

    # Save cleanly structured CSV without index column
    df.to_csv(CLEANED_CSV, index=False)
    print(f"[SUCCESS] Cleaned data saved successfully to {CLEANED_CSV}")

if __name__ == "__main__":
    clean_data()