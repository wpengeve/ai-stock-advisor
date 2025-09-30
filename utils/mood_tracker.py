import pandas as pd
from datetime import datetime
import os

MOOD_LOG_FILE = "macro_mood_log.csv"

def save_macro_mood(mood_text):
    # Determine if Risk-On or Risk-Off
    if "Risk-On" in mood_text:
        mood = "Risk-On"
    elif "Risk-Off" in mood_text:
        mood = "Risk-Off"
    else:
        mood = "Unknown"

    today = datetime.now().strftime("%Y-%m-%d")

    # If file exists, load it
    if os.path.exists(MOOD_LOG_FILE):
        df = pd.read_csv(MOOD_LOG_FILE)
    else:
        df = pd.DataFrame(columns=["date", "mood"])

    # Only save if today not already saved
    if not ((df["date"] == today) & (df["mood"] == mood)).any():
        df = pd.concat([df, pd.DataFrame({"date": [today], "mood": [mood]})], ignore_index=True)
        df.to_csv(MOOD_LOG_FILE, index=False)