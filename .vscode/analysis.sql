USE fraudshield;

-- Query 1: Total number of transactions
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- Query 2: Fraud vs Normal split with percentages
SELECT
    fraud_label,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM transactions
GROUP BY fraud_label;

-- Query 3: Top 10 customers by total transaction value
SELECT
    c.customer_id,
    c.home_location,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.transaction_amount) AS total_amount_millions,
    SUM(CASE WHEN t.fraud_label = 'Fraud' THEN 1 ELSE 0 END) AS fraud_count
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.home_location
ORDER BY total_amount_millions DESC
LIMIT 10;

-- Query 4: Monthly transaction trends
SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN fraud_label = 'Fraud' THEN 1 ELSE 0 END) AS fraud_count,
    ROUND(SUM(CASE WHEN fraud_label = 'Fraud' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY month
ORDER BY month ASC;

-- Query 5: Fraud rate by transaction type
SELECT
    transaction_type,
    COUNT(*) AS total,
    SUM(fraud_label = 'Fraud') AS fraud_count,
    ROUND(AVG(fraud_label = 'Fraud') * 100, 2) AS fraud_rate_pct
FROM transactions
GROUP BY transaction_type
ORDER BY fraud_rate_pct DESC;

-- Query 6: Fraud rate by merchant category
SELECT
    m.merchant_category,
    COUNT(*) AS total,
    SUM(t.fraud_label = 'Fraud') AS fraud_count,
    ROUND(AVG(t.fraud_label = 'Fraud') * 100, 2) AS fraud_rate_pct
FROM transactions t
JOIN merchants m ON t.merchant_id = m.merchant_id
GROUP BY m.merchant_category
ORDER BY fraud_rate_pct DESC;

-- Query 7: Suspicious pattern detection
SELECT
    t.original_transaction_id,
    t.transaction_amount,
    t.transaction_location,
    t.distance_from_home,
    t.is_international,
    fi.unusual_time_transaction,
    fi.failed_transaction_count,
    t.fraud_label
FROM transactions t
JOIN fraud_indicators fi ON t.original_transaction_id = fi.transaction_id
WHERE t.is_international = 'Yes'
AND fi.unusual_time_transaction = 'Yes'
AND t.distance_from_home > 300
ORDER BY t.distance_from_home DESC
LIMIT 50;