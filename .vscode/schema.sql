-- ============================================================
-- schema.sql
-- Phase 3 - Database Schema Creation
-- FraudShield Banking Data Project
-- ============================================================

DROP DATABASE IF EXISTS fraudshield;
CREATE DATABASE fraudshield;
USE fraudshield;

CREATE TABLE customers (
    customer_id         INT             NOT NULL,
    home_location       VARCHAR(100),
    PRIMARY KEY (customer_id)
);

CREATE TABLE merchants (
    merchant_id         INT             NOT NULL,
    merchant_category   VARCHAR(50),
    PRIMARY KEY (merchant_id)
);

CREATE TABLE transactions (
    transaction_id              INT             NOT NULL AUTO_INCREMENT,
    original_transaction_id     INT,
    customer_id                 INT             NOT NULL,
    merchant_id                 INT             NOT NULL,
    transaction_amount          DECIMAL(15, 2),
    transaction_time            TIME,
    transaction_date            DATE,
    transaction_type            ENUM('Online', 'ATM', 'POS'),
    transaction_location        VARCHAR(100),
    distance_from_home          DECIMAL(10, 2),
    device_id                   BIGINT,
    ip_address                  VARCHAR(45),
    card_type                   ENUM('Credit', 'Debit'),
    account_balance             DECIMAL(15, 2),
    daily_transaction_count     INT,
    weekly_transaction_count    INT,
    avg_transaction_amount      DECIMAL(15, 2),
    max_transaction_last_24h    DECIMAL(15, 2),
    is_international            ENUM('Yes', 'No'),
    fraud_label                 ENUM('Normal', 'Fraud') NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id),
    FOREIGN KEY (merchant_id)   REFERENCES merchants(merchant_id)
);

CREATE TABLE fraud_indicators (
    indicator_id                INT     NOT NULL AUTO_INCREMENT,
    transaction_id              INT,
    is_new_merchant             ENUM('Yes', 'No'),
    failed_transaction_count    INT     DEFAULT 0,
    unusual_time_transaction    ENUM('Yes', 'No'),
    previous_fraud_count        INT     DEFAULT 0,
    PRIMARY KEY (indicator_id)
);