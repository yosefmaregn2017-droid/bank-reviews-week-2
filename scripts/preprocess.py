# scripts/preprocess.py

import pandas as pd

# Load raw reviews
df = pd.read_csv("data/raw/bank_reviews_raw.csv")

# Step 1: Remove duplicates
df.drop_duplicates(subset=["review", "bank"], inplace=True)

# Step 2: Handle missing values
# Drop rows where 'review' or 'rating' is missing
df.dropna(subset=["review", "rating"], inplace=True)

# Step 3: Normalize dates
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df.dropna(subset=["date"], inplace=True)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Step 4: Save cleaned CSV
df.to_csv("data/processed/bank_reviews_cleaned.csv", index=False)
print("Saved cleaned reviews to data/processed/bank_reviews_cleaned.csv")
