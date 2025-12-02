import pandas as pd
import os

# Paths
raw_path = os.path.join('data', 'raw', 'bank_reviews_raw.csv')
processed_path = os.path.join('data', 'processed', 'bank_reviews_analysis.csv')

# Ensure processed folder exists
os.makedirs(os.path.dirname(processed_path), exist_ok=True)

# Read raw data
df = pd.read_csv(raw_path)

# Optional: basic cleaning (e.g., drop missing reviews)
df = df.dropna(subset=['review_text']) if 'review_text' in df.columns else df

# Save to processed CSV
df.to_csv(processed_path, index=False)

print(f"Processed CSV saved at: {processed_path}")
