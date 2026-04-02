import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqlconnector://root:Adejumoke123@localhost:3306/fraudshield')

# EXTRACT
df = pd.read_csv('FraudShield_Banking_Data.csv')
print(f"Loaded {len(df)} rows")

# TRANSFORM
df.columns = [
    'original_transaction_id', 'customer_id', 'transaction_amount',
    'transaction_time', 'transaction_date', 'transaction_type',
    'merchant_id', 'merchant_category', 'transaction_location',
    'home_location', 'distance_from_home', 'device_id', 'ip_address',
    'card_type', 'account_balance', 'daily_transaction_count',
    'weekly_transaction_count', 'avg_transaction_amount',
    'max_transaction_last_24h', 'is_international', 'is_new_merchant',
    'failed_transaction_count', 'unusual_time_transaction',
    'previous_fraud_count', 'fraud_label'
]

# Handle duplicates - keep first occurrence of each transaction_id
df = df.drop_duplicates(subset=['original_transaction_id'], keep='first')
print(f"After removing duplicates: {len(df)} rows")

# Handle missing values more carefully
df.dropna(subset=['customer_id', 'merchant_id', 'original_transaction_id'], inplace=True)
df['customer_id'] = df['customer_id'].astype(int)
df['merchant_id'] = df['merchant_id'].astype(int)
df['device_id'] = df['device_id'].astype('Int64')
df['original_transaction_id'] = df['original_transaction_id'].astype(int)
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce').dt.date
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M', errors='coerce').dt.time
df['failed_transaction_count'] = df['failed_transaction_count'].fillna(0).astype(int)
df['previous_fraud_count'] = df['previous_fraud_count'].fillna(0).astype(int)
df['fraud_label'] = df['fraud_label'].fillna('Normal')
print(f"Transform complete. {len(df)} rows ready.")

# SPLIT
customers = df[['customer_id', 'home_location']].drop_duplicates(subset='customer_id').reset_index(drop=True)
merchants = df[['merchant_id', 'merchant_category']].drop_duplicates(subset='merchant_id').reset_index(drop=True)
transactions = df[[
    'original_transaction_id', 'customer_id', 'merchant_id',
    'transaction_amount', 'transaction_time', 'transaction_date',
    'transaction_type', 'transaction_location', 'distance_from_home',
    'device_id', 'ip_address', 'card_type', 'account_balance',
    'daily_transaction_count', 'weekly_transaction_count',
    'avg_transaction_amount', 'max_transaction_last_24h',
    'is_international', 'fraud_label'
]].copy()
fraud_indicators = df[[
    'original_transaction_id', 'is_new_merchant',
    'failed_transaction_count', 'unusual_time_transaction',
    'previous_fraud_count'
]].copy().rename(columns={'original_transaction_id': 'transaction_id'})

print(f"Customers: {len(customers)} rows")
print(f"Merchants: {len(merchants)} rows")
print(f"Transactions: {len(transactions)} rows")
print(f"Fraud indicators: {len(fraud_indicators)} rows")

# LOAD - drop tables first to avoid foreign key issues, then disable checks
print("\nDropping existing tables...")
with engine.connect() as conn:
    # Drop tables in reverse dependency order
    conn.execute(text("DROP TABLE IF EXISTS fraud_indicators"))
    conn.execute(text("DROP TABLE IF EXISTS transactions"))
    conn.execute(text("DROP TABLE IF EXISTS customers"))
    conn.execute(text("DROP TABLE IF EXISTS merchants"))
    conn.commit()

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.commit()

print("Loading customers...")
customers.to_sql(name='customers', con=engine, if_exists='replace', index=False, chunksize=1000)
print(f"  Done: {len(customers)} rows")

print("Loading merchants...")
merchants.to_sql(name='merchants', con=engine, if_exists='replace', index=False, chunksize=1000)
print(f"  Done: {len(merchants)} rows")

print("Loading transactions...")
transactions.to_sql(name='transactions', con=engine, if_exists='replace', index=False, chunksize=1000)
print(f"  Done: {len(transactions)} rows")

print("Loading fraud_indicators...")
fraud_indicators.to_sql(name='fraud_indicators', con=engine, if_exists='replace', index=False, chunksize=1000)
print(f"  Done: {len(fraud_indicators)} rows")

# Re-enable foreign key checks
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()

# VERIFY
print("\nVerifying row counts...")
with engine.connect() as conn:
    for table in ['customers', 'merchants', 'transactions', 'fraud_indicators']:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        print(f"  {table}: {count} rows")

print("\nETL COMPLETE")