import pandas as pd
import psycopg2
from pathlib import Path

# Load data
data_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "bank_reviews_analysis.csv"
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} reviews")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="Kifiya@123",
    port=5432
)

cursor = conn.cursor()

# Insert query
insert_query = """
INSERT INTO reviews 
(bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Map bank name to bank_id
bank_map = {
    "CBE": 1,
    "BOA": 2,
    "Dashen": 3
}

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        bank_map.get(row['bank'], None),
        row['review'],
        row['rating'],
        row['date'],
        None,
        None,
        row['source']
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Inserted all reviews into PostgreSQL!")
