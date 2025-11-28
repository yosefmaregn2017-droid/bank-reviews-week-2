# scripts/store_in_postgres.py

import pandas as pd
import psycopg2

# Load analyzed CSV
df = pd.read_csv("data/processed/bank_reviews_analysis.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="YOUR_PASSWORD"  # replace with your PostgreSQL password
)
cur = conn.cursor()

# Insert unique banks
banks = df['bank'].unique()
bank_id_map = {}
for bank in banks:
    cur.execute("INSERT INTO banks (bank_name) VALUES (%s) RETURNING bank_id", (bank,))
    bank_id_map[bank] = cur.fetchone()[0]

# Insert reviews
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        bank_id_map[row['bank']],
        row['review'],
        row['rating'],
        row['date'],
        row['sentiment_label'],
        row['sentiment_score'],
        row['source']
    ))

conn.commit()
cur.close()
conn.close()

print("Data inserted into PostgreSQL successfully!")
