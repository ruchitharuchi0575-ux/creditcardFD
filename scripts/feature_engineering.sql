-- Create a comprehensive analytical view using SQL Window Functions and CTEs
CREATE OR REPLACE VIEW v_fraud_engineered_features AS
WITH transaction_windows AS (
    SELECT 
        transaction_id,
        user_id,
        transaction_timestamp,
        Amount,
        Class,
        
        -- 1. WINDOW FUNCTION: Previous Transaction Time Gap (detecting rapid velocity)
        LAG(transaction_timestamp, 1) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_timestamp
        ) AS prev_transaction_time,
        
        -- 2. WINDOW FUNCTION: 7-Day Rolling Average Spend per User
        AVG(Amount) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_timestamp
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_7d_amount,
        
        -- 3. WINDOW FUNCTION: Transaction Sequence Rank per User
        DENSE_RANK() OVER (
            PARTITION BY user_id 
            ORDER BY Amount DESC
        ) AS user_spend_rank

    FROM transactions
)
SELECT 
    tw.*,
    
    -- Calculate time difference in seconds between consecutive transactions
    EXTRACT(EPOCH FROM (tw.transaction_timestamp - tw.prev_transaction_time)) AS seconds_since_last_txn,
    
    -- Deviation from rolling average spending behavior
    CASE 
        WHEN tw.rolling_avg_7d_amount > 0 
        THEN (tw.Amount / tw.rolling_avg_7d_amount)
        ELSE 1.0 
    END AS amount_to_rolling_avg_ratio

FROM transaction_windows tw;