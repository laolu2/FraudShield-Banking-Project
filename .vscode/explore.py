# ============================================================
# explore.py
# Phase 1 - Data Understanding
# This script reads the CSV and prints everything you need
# to understand the dataset before building anything
# Run it with: python explore.py
# ============================================================

import pandas as pd

# Load the CSV file into a DataFrame
# Make sure FraudShield_Banking_Data.csv is in the same folder
df = pd.read_csv('FraudShield_Banking_Data.csv')


# --- Shape ---
# How many rows and columns exist
# Expected: (50000, 25)
print("=" * 50)
print("SHAPE (rows, columns):")
print(df.shape)


# --- Column names ---
# Lists all 25 column names
print("\n" + "=" * 50)
print("ALL COLUMN NAMES:")
for col in df.columns:
    print(" -", col)


# --- Data types ---
# Shows what Python thinks each column type is
# You will notice IDs are float64 - you fix this in ETL
print("\n" + "=" * 50)
print("DATA TYPES:")
print(df.dtypes)


# --- Missing values ---
# Any column with a number greater than 0 has missing data
print("\n" + "=" * 50)
print("MISSING VALUES PER COLUMN:")
print(df.isnull().sum())


# --- Basic statistics ---
# Min, max, mean for all numeric columns
print("\n" + "=" * 50)
print("BASIC STATISTICS:")
print(df.describe())


# --- Duplicate Transaction IDs ---
# Critical issue - 1361 duplicates found
# Means Transaction_ID cannot be used as primary key directly
print("\n" + "=" * 50)
print("DUPLICATE TRANSACTION IDs:")
print(df['Transaction_ID'].duplicated().sum())


# --- Unique counts ---
print("\n" + "=" * 50)
print("UNIQUE CUSTOMERS:", df['Customer_ID'].nunique())
print("UNIQUE MERCHANTS:", df['Merchant_ID'].nunique())


# --- Fraud breakdown ---
# Expected: Normal 47573, Fraud 2423 (4.85% fraud rate)
print("\n" + "=" * 50)
print("FRAUD LABEL COUNTS:")
print(df['Fraud_Label'].value_counts())
print("FRAUD RATE %:", round(df['Fraud_Label'].eq('Fraud').mean() * 100, 2))


# --- Categorical column values ---
# Shows all possible values in each category column
print("\n" + "=" * 50)
print("TRANSACTION TYPES:")
print(df['Transaction_Type'].value_counts())

print("\nMERCHANT CATEGORIES:")
print(df['Merchant_Category'].value_counts())

print("\nCARD TYPES:")
print(df['Card_Type'].value_counts())

print("\nIS INTERNATIONAL:")
print(df['Is_International_Transaction'].value_counts())

print("\nIS NEW MERCHANT:")
print(df['Is_New_Merchant'].value_counts())

print("\nUNUSUAL TIME:")
print(df['Unusual_Time_Transaction'].value_counts())


# --- Date range ---
df['Transaction_Date'] = pd.to_datetime(
    df['Transaction_Date'], errors='coerce')
print("\n" + "=" * 50)
print("DATE RANGE:")
print("Earliest:", df['Transaction_Date'].min())
print("Latest:  ", df['Transaction_Date'].max())


# --- Fraud signals ---
# Shows fraud rate broken down by key columns
print("\n" + "=" * 50)
print("FRAUD RATE BY INTERNATIONAL:")
print(df.groupby('Is_International_Transaction')['Fraud_Label']
      .value_counts(normalize=True).unstack().round(4))

print("\nFRAUD RATE BY UNUSUAL TIME:")
print(df.groupby('Unusual_Time_Transaction')['Fraud_Label']
      .value_counts(normalize=True).unstack().round(4))

print("\nFRAUD RATE BY TRANSACTION TYPE:")
print(df.groupby('Transaction_Type')['Fraud_Label']
      .value_counts(normalize=True).unstack().round(4))


print("\n" + "=" * 50)
print("Exploration complete.")