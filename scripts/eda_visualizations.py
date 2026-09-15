from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# Path setup
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "fraud_db.db"
OUTPUT_DIR = BASE_DIR / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Database Connection
engine = create_engine(f"sqlite:///{DB_PATH}")


def generate_eda_plots():
    # Load feature-engineered view directly from SQLite
    query = "SELECT * FROM v_fraud_engineered_features"
    df = pd.read_sql(query, engine)

    # Set aesthetics
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Transaction Amount Distribution (Log Scale) by Class
    sns.boxplot(
        ax=axes[0, 0],
        data=df,
        x="Class",
        y="Amount",
        hue="Class",
        palette="Set2",
    )
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_title("Log Transaction Amount by Fraud Class (0=Legit, 1=Fraud)")
    axes[0, 0].set_xlabel("Class")

    # 2. Velocity Risk: Seconds Since Last Transaction
    sns.kdeplot(
        ax=axes[0, 1],
        data=df,
        x="seconds_since_last_txn",
        hue="Class",
        common_norm=False,
        palette="magma",
        fill=True,
    )
    axes[0, 1].set_title("Transaction Velocity (Seconds Since Prev Transaction)")
    axes[0, 1].set_xlim(0, 3600)  # Zoom in on first hour

    # 3. Ratio of Amount to 7-Day Rolling Average
    sns.histplot(
        ax=axes[1, 0],
        data=df,
        x="amount_to_rolling_avg_ratio",
        hue="Class",
        bins=20,
        multiple="stack",
    )
    axes[1, 0].set_title("Deviation Ratio vs 7-Day Rolling Spend")

    # 4. User Spend Rank Distribution
    sns.countplot(
        ax=axes[1, 1],
        data=df[df["Class"] == 1],
        x="user_spend_rank",
        color="crimson",
    )
    axes[1, 1].set_title("Rank of Fraudulent Transactions in User History")

    plt.tight_layout()
    plot_file = OUTPUT_DIR / "eda_fraud_analysis.png"
    plt.savefig(plot_file, dpi=300)
    print(f"EDA Visualizations saved successfully to: {plot_file}")


if __name__ == "__main__":
    generate_eda_plots()