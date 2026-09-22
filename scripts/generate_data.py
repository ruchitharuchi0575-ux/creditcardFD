import sqlite3
import random
import os

def generate_bulk_transactions(num_records=500):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/fraud_predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            Amount REAL,
            fraud_probability REAL,
            risk_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    records = []
    for _ in range(num_records):
        user_id = random.randint(1000, 9999)
        amount = round(random.uniform(5.0, 2500.0), 2)
        
        if random.random() < 0.05:
            fraud_prob = round(random.uniform(0.85, 0.99), 4)
            risk_level = "HIGH RISK"
        else:
            fraud_prob = round(random.uniform(0.00, 0.20), 4)
            risk_level = "LOW RISK"

        records.append((user_id, amount, fraud_prob, risk_level))

    cursor.executemany("""
        INSERT INTO predictions (user_id, Amount, fraud_probability, risk_level)
        VALUES (?, ?, ?, ?)
    """, records)

    conn.commit()
    conn.close()
    print(f"✅ Inserted {num_records} transactions into data/fraud_predictions.db")

if __name__ == "__main__":
    generate_bulk_transactions(500)