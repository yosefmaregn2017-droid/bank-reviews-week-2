from google_play_scraper import reviews, Sort
import pandas as pd
from tqdm import tqdm

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.bankb.app",
    "DashnBank": "com.boa.boaMobileBanking"
}

all_reviews = []

for bank_name, app_id in apps.items():
    print(f"Scraping reviews for {bank_name}...")
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=500
    )
    
    for r in result:
        all_reviews.append({
            "review": r['content'],
            "rating": r['score'],
            "date": r['at'].strftime('%Y-%m-%d'),
            "bank": bank_name,
            "source": "Google Play"
        })

df = pd.DataFrame(all_reviews)
df.to_csv("data/raw/bank_reviews_raw.csv", index=False)
print("Saved raw reviews to data/raw/bank_reviews_raw.csv")
