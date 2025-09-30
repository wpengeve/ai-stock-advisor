# data_sources/macro_news.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_macro_headlines(limit=5):
    """
    Fetch top recent macroeconomic/general news from Finnhub.
    """
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        news = response.json()

        # Filter top relevant headlines
        top_news = news[:limit]
        headlines = [item['headline'] for item in top_news if 'headline' in item]
        return headlines

    except Exception as e:
        print(f"⚠️ Error fetching macro news: {e}")
        return []