import requests
import os
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def fetch_earnings_for_stock(ticker):
    """
    Fetch the most recent earnings report for a given stock using the Finnhub API.
    """
    url = f"https://finnhub.io/api/v1/stock/earnings?symbol={ticker}&token={FINNHUB_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        latest = data[0]  # Get the most recent earnings result
        return {
            "ticker": ticker.upper(),
            "earnings_date": latest["period"],
            "revenue": "N/A",  # Finnhub doesn't provide revenue here
            "revenue_surprise": "N/A",
            "eps": latest["actual"],
            "eps_estimate": latest["estimate"],
            "eps_surprise": latest.get("surprise"),
            "eps_surprise_percent": latest.get("surprisePercent"),
            "notes": f"Reported on {latest['period']} with EPS {'above' if latest['actual'] > latest['estimate'] else 'below'} expectations."
        }

    except Exception as e:
        print(f"⚠️ Error fetching earnings for {ticker}: {e}")
        return None

