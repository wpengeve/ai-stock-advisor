import requests
import os
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_recent_headlines(ticker):
    """
    Uses NewsAPI to fetch recent headlines about a stock ticker.
    """
    api_key = os.getenv("NEWS_API_KEY")
    company_name = ticker.upper()

    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Error fetching news: {response.status_code}")
        return [f"No news found for {ticker}"]

    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles]

    return headlines if headlines else [f"No recent news found for {ticker}"]

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_google_news_headlines(ticker):
    """
    Scrapes Google News for recent headlines.
    """
    search_url = f"https://www.google.com/search?q={ticker}+stock+news&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")

    headlines = [item.get_text() for item in results[:5]]
    return headlines if headlines else [f"No Google headlines found for {ticker}"]

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_all_headlines(ticker):
    """
    Combines headlines from NewsAPI and Google News
    """
    # Use a simple approach - the caching will prevent repeated prints anyway
    # The print statements will only show once per unique ticker due to caching
    print(f"📰 Fetching news headlines for {ticker}...")
    
    newsapi_headlines = get_recent_headlines(ticker)
    google_headlines = get_google_news_headlines(ticker)

    combined = list(dict.fromkeys(newsapi_headlines + google_headlines))  # removes duplicates
    return combined[:7]  # limit to top 7 headlines total