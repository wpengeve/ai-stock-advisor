import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import yfinance as yf
import time

CACHE = {}

def get_stock_summary(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="5d")
        info = ticker.info

        return {
            "price": info.get("regularMarketPrice"),
            "name": info.get("shortName", ticker_symbol),
            "history": hist
        }
    except Exception as e:
        return {
            "price": None,
            "name": ticker_symbol,
            "history": None,
            "error": str(e)
        }

def get_trending_stocks(limit=10):
    """
    Scrapes Yahoo Finance Trending Tickers
    """
    url = "https://finance.yahoo.com/trending-tickers"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table")

    tickers = []
    if table:
        rows = table.find_all("tr")[1:]  # skip header row
        for row in rows[:limit]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()
                tickers.append((symbol, name))

    return tickers

def get_cached_stock_summary(ticker):
    if ticker in CACHE and not is_stale(CACHE[ticker]):
        return CACHE[ticker]

    time.sleep(7.5)  # throttle to avoid API limit
    stock_info = get_stock_summary(ticker)
    CACHE[ticker] = stock_info
    return stock_info

def is_stale(entry, ttl_seconds=3600):
    return (datetime.utcnow() - entry["timestamp"]).total_seconds() > ttl_seconds