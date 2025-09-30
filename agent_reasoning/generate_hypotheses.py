def generate_investment_hypothesis(macro_mood, earnings_result, price_trend_percent):
    """
    Return a 3-layer reasoning output like a real financial advisor:
    - Market mood
    - Company performance
    - Investment takeaway
    """

    mood_line = ""
    earnings_line = ""
    price_line = ""
    conclusion = ""

    # 🟢 1. Macro Mood
    if macro_mood == "Risk-On":
        mood_line = "🟢 *Risk-On* mood detected — investors are optimistic and buying riskier assets."
    elif macro_mood == "Risk-Off":
        mood_line = "🔴 *Risk-Off* mood detected — investors are cautious and shifting to safer assets."
    else:
        mood_line = "⚪️ Market mood is unclear today."

    # 📊 2. Earnings
    if earnings_result == "Beat":
        earnings_line = "✅ The company recently beat earnings expectations."
    elif earnings_result == "Miss":
        earnings_line = "❌ The company recently missed earnings expectations."
    else:
        earnings_line = "ℹ️ Earnings results are neutral or not available."

    # 📈 3. Price Trend
    if price_trend_percent > 3:
        price_line = f"📈 The stock is up {price_trend_percent:.2f}% in the past 5 days — strong upward momentum."
    elif price_trend_percent < -3:
        price_line = f"📉 The stock is down {abs(price_trend_percent):.2f}% in the past 5 days — showing weakness."
    else:
        price_line = f"➡️ Price moved {price_trend_percent:.2f}% in the past 5 days — relatively stable."

    # 💡 4. Conclusion
    if macro_mood == "Risk-On" and earnings_result == "Beat" and price_trend_percent > 3:
        conclusion = "📣 Outlook: Strong bullish setup. Investors may consider short-term entries or holding positions."
    elif macro_mood == "Risk-Off" and earnings_result == "Miss" and price_trend_percent < -3:
        conclusion = "⚠️ Outlook: Weak signals. Investors may want to stay cautious or avoid for now."
    else:
        conclusion = "🧭 Outlook: Mixed signals. Consider watching the stock for stronger confirmation before taking action."

    return f"{mood_line}\n\n{earnings_line}\n{price_line}\n\n{conclusion}"