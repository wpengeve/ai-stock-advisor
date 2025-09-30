from fpdf import FPDF
from datetime import datetime
import requests
import pickle
import os
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

US_TICKERS_FILE = "us_tickers.pkl"

def sanitize_text(text):
    """
    Remove characters that aren't compatible with latin-1 encoding (e.g., emojis).
    """
    return text.encode("latin-1", errors="ignore").decode("latin-1")

def generate_pdf_report(summaries, risk_analysis, filename="report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, sanitize_text("AI Stock Comparison Report"), ln=True)

    # Date
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, sanitize_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)

    # Stock Summaries
    for ticker, summary in summaries:
        pdf.set_font("Arial", "B", 14)
        pdf.ln(10)
        pdf.cell(0, 10, sanitize_text(f"{ticker} Summary"), ln=True)

        pdf.set_font("Arial", "", 11)
        for line in summary.split("\n"):
            pdf.multi_cell(0, 8, sanitize_text(line))

    # GPT Risk Comparison
    pdf.set_font("Arial", "B", 14)
    pdf.ln(10)
    pdf.cell(0, 10, sanitize_text("Risk Analysis"), ln=True)

    pdf.set_font("Arial", "", 11)
    for line in risk_analysis.split("\n"):
        pdf.multi_cell(0, 8, sanitize_text(line))

    # Save the PDF
    pdf.output(filename)

def fetch_and_cache_us_tickers():
    """
    Fetches all US-listed stock symbols from Finnhub and caches them locally.
    If cached data exists, it loads from file instead of making a new API call.
    """
    if os.path.exists(US_TICKERS_FILE):
        with open(US_TICKERS_FILE, "rb") as f:
            return pickle.load(f)

    if not FINNHUB_API_KEY:
        raise ValueError("⚠️ FINNHUB_API_KEY is not set in the environment.")

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    us_tickers = set(item["symbol"] for item in data if item.get("mic") in {"XNYS", "XNAS", "ARCX"})

    with open(US_TICKERS_FILE, "wb") as f:
        pickle.dump(us_tickers, f)

    return us_tickers

def is_us_stock(symbol, us_ticker_set):
    """
    Checks if the given symbol exists in the set of US-listed tickers.
    """
    return symbol.upper() in us_ticker_set