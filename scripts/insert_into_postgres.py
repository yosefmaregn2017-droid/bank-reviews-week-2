import pandas as pd
import psycopg2
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the cleaned + sentiment + theme data
data_path = BASE_DIR / "data" / "reviews_with_themes.csv"
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} reviews")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",        # change if needed
    password="Kifiya@123",  # your password
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
        bank_map.get(row['bank'], None),   # safer
        row['review'],
        row.get('rating', None),
        row.get('date', None),
        row['sentiment_label'],
        row['sentiment_score'],
        "Google Play"
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Inserted all reviews into PostgreSQL!")
