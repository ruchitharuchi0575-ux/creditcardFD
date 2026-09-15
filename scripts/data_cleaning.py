import pandas as pd
import numpy as np
from pathlib import Path

# Locate the data folder
BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in locals() else Path.cwd()
data_dir = BASE_DIR / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# Generate synthetic credit card data
np.random.seed(42)
n_rows = 100

df_mock = pd.DataFrame({
    'user_id': np.random.randint(1000, 1050, size=n_rows),
    'Time': np.sort(np.random.randint(0, 86400, size=n_rows)),
    'Amount': np.round(np.random.exponential(scale=50, size=n_rows), 2),
    'Class': np.random.choice([0, 1], size=n_rows, p=[0.95, 0.05])  # 5% fraud
})

# Save to raw_transactions.csv
file_path = data_dir / "raw_transactions.csv"
df_mock.to_csv(file_path, index=False)

print(f" Successfully generated mock data at: {file_path}")