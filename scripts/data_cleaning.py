import pandas as pd
import numpy as np

def clean_transaction_data(file_path: str) -> pd.DataFrame:
    """Reads, cleans, and pre-processes raw credit card transaction data."""
    # 1. Ingest raw CSV data
    df = pd.read_csv(file_path)
    
    # 2. Handle & parse timestamps
    df['transaction_timestamp'] = pd.to_datetime(df['Time'], unit='s', origin='2026-01-01')
    
    # 3. Clean Missing Values
    # Impute missing transaction amounts with median, flag missing user IDs
    df['Amount'] = df['Amount'].fillna(df['Amount'].median())
    
    # 4. Feature Transformations (NumPy)
    # Log-transform transaction amounts to mitigate skewed outlier impacts
    df['log_amount'] = np.log1p(df['Amount'])
    
    # Standardize scale for amounts using Z-score
    amount_mean = df['Amount'].mean()
    amount_std = df['Amount'].std()
    df['amount_zscore'] = (df['Amount'] - amount_mean) / amount_std
    
    # 5. Extract Time-Based Features
    df['hour_of_day'] = df['transaction_timestamp'].dt.hour
    df['day_of_week'] = df['transaction_timestamp'].dt.dayofweek
    
    return df

if __name__ == "__main__":
    raw_path = "../data/raw_transactions.csv"
    cleaned_df = clean_transaction_data(raw_path)
    cleaned_df.to_csv("../data/cleaned_transactions.csv", index=False)
    print(f"Data successfully cleaned. Rows processed: {len(cleaned_df)}")