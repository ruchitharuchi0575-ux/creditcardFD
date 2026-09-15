DROP VIEW IF EXISTS v_fraud_engineered_features;

CREATE VIEW v_fraud_engineered_features AS
WITH transaction_windows AS (
    SELECT 
        user_id,
        transaction_timestamp,
        Amount,
        Class,

        LAG(transaction_timestamp, 1) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_timestamp
        ) AS prev_transaction_time,

        AVG(Amount) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_timestamp
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_7d_amount,

        DENSE_RANK() OVER (
            PARTITION BY user_id 
            ORDER BY Amount DESC
        ) AS user_spend_rank

    FROM transactions
)
SELECT 
    tw.*,
    (unixepoch(tw.transaction_timestamp) - unixepoch(tw.prev_transaction_time)) AS seconds_since_last_txn,
    CASE 
        WHEN tw.rolling_avg_7d_amount > 0 
        THEN (tw.Amount / tw.rolling_avg_7d_amount)
        ELSE 1.0 
    END AS amount_to_rolling_avg_ratio
FROM transaction_windows tw;