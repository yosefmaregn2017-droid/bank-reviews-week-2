# scripts/preprocess.py

import pandas as pd

# Load raw reviews
df = pd.read_csv("data/raw/bank_reviews_raw.csv")

# Drop duplicates
df = df.drop_duplicates(subset=['review'])

# Handle missing values
df = df.dropna(subset=['review', 'rating', 'date', 'bank', 'source'])

# Normalize date to YYYY-MM-DD
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Save cleaned CSV
df.to_csv("data/processed/bank_reviews_cleaned.csv", index=False)
print("Cleaned CSV saved to data/processed/bank_reviews_cleaned.csv")
