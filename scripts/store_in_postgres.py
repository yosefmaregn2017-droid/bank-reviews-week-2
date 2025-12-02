from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd

# Load cleaned CSV (from Task 1 & 2)
df = pd.read_csv("cleaned_reviews.csv")  # Columns: bank_name, review_text, review_date, rating, sentiment_score, theme

# Database connection
DB_USER = 'bank_reviews'         # Your PostgreSQL username
DB_PASSWORD = 'Kifiya@123'       # Your PostgreSQL password
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bank_reviews'

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Define tables
class Bank(Base):
    __tablename__ = 'banks'
    bank_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    reviews = relationship("Review", back_populates="bank")

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.bank_id'))
    review_text = Column(Text)
    review_date = Column(Date)
    rating = Column(Integer)
    sentiment_score = Column(Float)
    theme = Column(String(255))

    bank = relationship("Bank", back_populates="reviews")

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert banks and build bank mapping
bank_map = {}
for bank_name in df['bank_name'].unique():
    bank = Bank(name=bank_name)
    session.add(bank)
    session.flush()  # Get bank_id without committing
    bank_map[bank_name] = bank.bank_id

# Insert reviews
for _, row in df.iterrows():
    review = Review(
        bank_id=bank_map[row['bank_name']],
        review_text=row['review_text'],
        review_date=row['review_date'],
        rating=row['rating'],
        sentiment_score=row['sentiment_score'],
        theme=row['theme']
    )
    session.add(review)

# Commit and close session
session.commit()
session.close()

print("Data inserted successfully using SQLAlchemy!")

