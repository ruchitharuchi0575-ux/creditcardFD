import pandas as pd
from sqlalchemy import create_engine, Integer, Float, DateTime, String

# PostgreSQL Database Connection
DB_URI = "postgresql://postgres:yourpassword@localhost:5432/fraud_db"
engine = create_engine(DB_URI)

def load_to_sql(csv_path: str):
    df = pd.read_csv(csv_path)
    
    # Define explicit schema datatypes
    dtype_mapping = {
        'Time': Float(),
        'Amount': Float(),
        'Class': Integer(),
        'log_amount': Float(),
        'amount_zscore': Float(),
        'hour_of_day': Integer(),
        'day_of_week': Integer(),
        'transaction_timestamp': DateTime()
    }
    
    df.to_sql(
        name='transactions',
        con=engine,
        if_exists='replace',
        index=False,
        dtype=dtype_mapping
    )
    print("Database table 'transactions' created and populated successfully.")

if __name__ == "__main__":
    load_to_sql("../data/cleaned_transactions.csv")