# scripts/sentiment_theme_analysis.py

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load cleaned reviews
df = pd.read_csv("data/processed/bank_reviews_cleaned.csv")

# Sentiment Analysis
sia = SentimentIntensityAnalyzer()

def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

df['sentiment_score'] = df['review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
df['sentiment_label'] = df['sentiment_score'].apply(get_sentiment_label)

# Thematic Analysis
themes = {
    "UI/UX": ["interface", "design", "navigation", "layout", "user experience", "ui"],
    "Transactions": ["transfer", "payment", "transaction", "deposit", "withdrawal"],
    "Customer Support": ["support", "help", "service", "call", "response", "chat"],
    "Performance": ["slow", "crash", "bug", "freeze", "lag"],
    "Security": ["password", "login", "security", "safe", "fraud"]
}

def identify_themes(review_text):
    review_text_lower = str(review_text).lower()
    assigned = [theme for theme, keywords in themes.items() if any(k in review_text_lower for k in keywords)]
    return ", ".join(assigned) if assigned else "Other"

df['themes'] = df['review'].apply(identify_themes)

# Save analysis results
df.to_csv("data/processed/bank_reviews_analysis.csv", index=False)
print("Sentiment and theme analysis saved to data/processed/bank_reviews_analysis.csv")

