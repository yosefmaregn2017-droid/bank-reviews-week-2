import psycopg2
import pandas as pd

# Load your cleaned CSV
df = pd.read_csv("cleaned_reviews.csv")  # Output from Task 1 & 2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",  # or your user
    password="your_password"
)
cur = conn.cursor()

# Insert banks into banks table (avoiding duplicates)
banks = df['bank_name'].unique()
for bank in banks:
    cur.execute("""
        INSERT INTO banks (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (bank,))

# Insert reviews
for idx, row in df.iterrows():
    # Get bank_id
    cur.execute("SELECT bank_id FROM banks WHERE name=%s", (row['bank_name'],))
    bank_id = cur.fetchone()[0]
    
    cur.execute("""
        INSERT INTO reviews (bank_id, review_text, review_date, rating, sentiment_score, theme)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        bank_id,
        row['review_text'],
        row['review_date'],
        row['rating'],
        row['sentiment_score'],
        row['theme']
    ))

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")
