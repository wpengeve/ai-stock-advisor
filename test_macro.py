import sys
import os

# 🔥 Correct sys.path fix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# 🔥 Now import safely
from data_sources.macro_news import get_macro_headlines

headlines = get_macro_headlines()

for i, headline in enumerate(headlines, start=1):
    print(f"{i}. {headline}")

