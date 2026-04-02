USE fraudshield;

CREATE INDEX idx_fraud_label
    ON transactions(fraud_label);

CREATE INDEX idx_transaction_date
    ON transactions(transaction_date);

CREATE INDEX idx_txn_customer_id
    ON transactions(customer_id);

CREATE INDEX idx_txn_merchant_id
    ON transactions(merchant_id);

CREATE INDEX idx_fi_transaction_id
    ON fraud_indicators(transaction_id);

CREATE INDEX idx_failed_count
    ON fraud_indicators(failed_transaction_count);

SHOW INDEX FROM transactions;
SHOW INDEX FROM fraud_indicators;