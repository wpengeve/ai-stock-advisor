from data_sources.earnings_reports import fetch_earnings_for_stock

result = fetch_earnings_for_stock("TSLA")
print(result)