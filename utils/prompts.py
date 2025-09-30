# utils/prompts.py

def get_stock_summary_prompt(ticker, company_name, price, price_change, headlines):
    headlines_text = "\n".join(f"- {headline}" for headline in headlines)

    prompt = f"""
You are an AI financial analyst assistant.

Summarize the recent activity for {company_name} ({ticker}).

- Current stock price: ${price:.2f}
- 5-day price change: {price_change:.2f}%

Recent news headlines:
{headlines_text}

Focus on any important developments, earnings reports, or news that might affect the stock price. 
Keep it concise and easy for a non-expert investor to understand.
"""
    return prompt

