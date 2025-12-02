from sqlalchemy import create_engine
import pandas as pd

# Connect to your PostgreSQL database
engine = create_engine("postgresql+psycopg2://bank_reviews:Kifiya@123@localhost:5432/bank_reviews")

# Check banks table
banks_df = pd.read_sql("SELECT * FROM banks", engine)
print("Banks table:")
print(banks_df)

# Check first 10 rows of reviews table
reviews_df = pd.read_sql("SELECT * FROM reviews LIMIT 10", engine)
print("\nReviews table (first 10 rows):")
print(reviews_df)
