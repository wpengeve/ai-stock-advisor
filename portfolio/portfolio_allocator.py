import yfinance as yf
from typing import List, Dict, Optional
import time


def fetch_current_prices(tickers: List[str]) -> Dict[str, float]:
    """
    Fetch current prices for a list of tickers using yfinance.
    Returns a dict: {ticker: price}
    """
    prices = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            price = info.get("regularMarketPrice")
            if price is not None:
                prices[ticker] = price
        except Exception:
            prices[ticker] = None
    return prices


def search_companies(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search for companies by name and return matching results with tickers.
    
    Args:
        query: Company name to search for
        max_results: Maximum number of results to return
    
    Returns:
        List of dicts: [{"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"}]
    """
    if not query or len(query) < 1:
        return []
    
    query = query.lower().strip()
    
    # Get popular stocks for local search
    popular_stocks = get_popular_stocks()
    matches = []
    
    # Search in popular stocks first (faster and more reliable)
    for stock in popular_stocks:
        stock_name = stock['name'].lower()
        stock_ticker = stock['ticker'].lower()
        
        # Check if query matches ticker or company name
        if (query in stock_ticker or 
            query in stock_name or
            stock_ticker.startswith(query) or
            stock_name.startswith(query) or
            any(word.startswith(query) for word in stock_name.split())):
            matches.append(stock)
    
    # Sort by relevance (exact matches first, then partial matches)
    def sort_key(stock):
        stock_name = stock['name'].lower()
        stock_ticker = stock['ticker'].lower()
        
        # Exact ticker match gets highest priority
        if stock_ticker == query:
            return 0
        # Ticker starts with query
        elif stock_ticker.startswith(query):
            return 1
        # Company name starts with query
        elif stock_name.startswith(query):
            return 2
        # Contains query
        else:
            return 3
    
    matches.sort(key=sort_key)
    
    # Return top matches
    return matches[:max_results]


def get_popular_stocks() -> List[Dict]:
    """
    Return a list of popular stocks for quick reference.
    """
    popular_stocks = [
        {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
        {"ticker": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
        {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
        {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical"},
        {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical"},
        {"ticker": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology"},
        {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology"},
        {"ticker": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
        {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services"},
        {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare"},
        {"ticker": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Defensive"},
        {"ticker": "TGT", "name": "Target Corporation", "sector": "Consumer Cyclical"},
        {"ticker": "WMT", "name": "Walmart Inc.", "sector": "Consumer Defensive"},
        {"ticker": "HD", "name": "Home Depot Inc.", "sector": "Consumer Cyclical"},
        {"ticker": "DIS", "name": "Walt Disney Co.", "sector": "Communication Services"},
        {"ticker": "KO", "name": "Coca-Cola Co.", "sector": "Consumer Defensive"},
        {"ticker": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Defensive"},
        {"ticker": "V", "name": "Visa Inc.", "sector": "Financial Services"},
        {"ticker": "MA", "name": "Mastercard Inc.", "sector": "Financial Services"},
        {"ticker": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare"},
        {"ticker": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare"},
        {"ticker": "ABT", "name": "Abbott Laboratories", "sector": "Healthcare"},
        {"ticker": "MRK", "name": "Merck & Co. Inc.", "sector": "Healthcare"},
        {"ticker": "TMO", "name": "Thermo Fisher Scientific Inc.", "sector": "Healthcare"},
        {"ticker": "AVGO", "name": "Broadcom Inc.", "sector": "Technology"},
        {"ticker": "CRM", "name": "Salesforce Inc.", "sector": "Technology"},
        {"ticker": "ADBE", "name": "Adobe Inc.", "sector": "Technology"},
        {"ticker": "ORCL", "name": "Oracle Corporation", "sector": "Technology"},
        {"ticker": "INTC", "name": "Intel Corporation", "sector": "Technology"},
        {"ticker": "AMD", "name": "Advanced Micro Devices Inc.", "sector": "Technology"},
        {"ticker": "QCOM", "name": "Qualcomm Inc.", "sector": "Technology"},
        {"ticker": "CSCO", "name": "Cisco Systems Inc.", "sector": "Technology"},
        {"ticker": "IBM", "name": "International Business Machines Corp.", "sector": "Technology"},
        {"ticker": "BA", "name": "Boeing Co.", "sector": "Industrials"},
        {"ticker": "CAT", "name": "Caterpillar Inc.", "sector": "Industrials"},
        {"ticker": "GE", "name": "General Electric Co.", "sector": "Industrials"},
        {"ticker": "MMM", "name": "3M Co.", "sector": "Industrials"},
        {"ticker": "HON", "name": "Honeywell International Inc.", "sector": "Industrials"},
        {"ticker": "XOM", "name": "Exxon Mobil Corp.", "sector": "Energy"},
        {"ticker": "CVX", "name": "Chevron Corporation", "sector": "Energy"},
        {"ticker": "COP", "name": "ConocoPhillips", "sector": "Energy"},
        {"ticker": "SLB", "name": "Schlumberger Ltd.", "sector": "Energy"},
        {"ticker": "EOG", "name": "EOG Resources Inc.", "sector": "Energy"},
    ]
    return popular_stocks


def get_stock_sectors(tickers: List[str]) -> Dict[str, str]:
    """
    Fetch sector information for a list of tickers using yfinance.
    Returns a dict: {ticker: sector}
    """
    sectors = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            sector = info.get("sector", "Unknown")
            sectors[ticker] = sector
        except Exception:
            sectors[ticker] = "Unknown"
    return sectors


def is_tech_stock(sector: str) -> bool:
    """
    Determine if a stock is in the technology sector based on its sector name.
    """
    tech_keywords = [
        "technology", "software", "semiconductor", "internet", 
        "computer", "electronics", "telecommunications", "tech"
    ]
    return any(keyword in sector.lower() for keyword in tech_keywords)


def allocate_portfolio_with_sector_preference(
    budget: float,
    tickers: List[str],
    prices: Dict[str, float],
    tech_preference: float = 0.6,
    custom_weights: Optional[Dict[str, float]] = None
) -> List[Dict]:
    """
    Allocate budget across tickers with sector-based weighting.
    
    Args:
        budget: Total budget to allocate
        tickers: List of stock tickers
        prices: Dict of current prices {ticker: price}
        tech_preference: Percentage of budget to allocate to tech stocks (0.0 to 1.0)
        custom_weights: Optional custom weights per stock (overrides sector preference)
    
    Returns:
        List of dicts: [{ticker, price, weight, allocated, shares, sector, is_tech}]
    """
    if not tickers:
        return []
    
    # Get sector information
    sectors = get_stock_sectors(tickers)
    
    # Separate tech and non-tech stocks
    tech_stocks = [t for t in tickers if is_tech_stock(sectors.get(t, "Unknown"))]
    non_tech_stocks = [t for t in tickers if not is_tech_stock(sectors.get(t, "Unknown"))]
    
    # If custom weights provided, use them instead of sector preference
    if custom_weights:
        print(f"Debug - Using custom weights: {custom_weights}")
        total_weight = sum(custom_weights.values())
        print(f"Debug - Total weight before normalization: {total_weight}")
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in custom_weights.items()}
        else:
            weights = {ticker: 1/len(tickers) for ticker in tickers}
        print(f"Debug - Normalized weights: {weights}")
    else:
        # Apply sector-based weighting
        weights = {}
        
        if tech_stocks and non_tech_stocks:
            # Allocate tech_preference to tech stocks, rest to non-tech
            tech_weight_per_stock = tech_preference / len(tech_stocks)
            non_tech_weight_per_stock = (1 - tech_preference) / len(non_tech_stocks)
            
            for ticker in tech_stocks:
                weights[ticker] = tech_weight_per_stock
            for ticker in non_tech_stocks:
                weights[ticker] = non_tech_weight_per_stock
                
        elif tech_stocks:
            # All stocks are tech
            weight_per_stock = 1.0 / len(tech_stocks)
            for ticker in tech_stocks:
                weights[ticker] = weight_per_stock
                
        elif non_tech_stocks:
            # All stocks are non-tech
            weight_per_stock = 1.0 / len(non_tech_stocks)
            for ticker in non_tech_stocks:
                weights[ticker] = weight_per_stock
        else:
            # Fallback to equal weighting
            weight_per_stock = 1.0 / len(tickers)
            for ticker in tickers:
                weights[ticker] = weight_per_stock
    
    # Calculate allocation
    allocation = []
    total_allocated = 0
    
    for ticker in tickers:
        price = prices.get(ticker)
        weight = weights.get(ticker, 0)
        
        if price and price > 0:
            # Calculate target allocation based on weight
            target_allocation = budget * weight
            
            # Smart allocation: Try to use more budget if other stocks can't use theirs
            # Calculate shares (integer division)
            shares = int(target_allocation // price)
            allocated = shares * price
            
            # Calculate what we could buy with fractional shares
            fractional_shares = target_allocation / price
            fractional_allocated = target_allocation
            
            # If we can't buy any shares, show the fractional option
            if shares == 0 and fractional_shares > 0:
                print(f"Debug - {ticker}: Target=${target_allocation:.2f}, Price=${price:.2f}, Fractional shares={fractional_shares:.2f}")
        else:
            shares = 0
            allocated = 0
            fractional_shares = 0
            fractional_allocated = 0
        
        sector = sectors.get(ticker, "Unknown")
        is_tech = is_tech_stock(sector)
        
        total_allocated += allocated
        
        allocation.append({
            "ticker": ticker,
            "price": price,
            "weight": weight,
            "allocated": allocated,
            "shares": shares,
            "fractional_shares": fractional_shares if shares == 0 else shares,
            "fractional_allocated": fractional_allocated if shares == 0 else allocated,
            "sector": sector,
            "is_tech": is_tech
        })
    
    # Budget redistribution: Try to use unused budget more efficiently
    unused_budget = budget - total_allocated
    if unused_budget > budget * 0.1:  # If more than 10% unused
        print(f"Debug - Attempting budget redistribution for unused ${unused_budget:.2f}")
        
        # Find stocks that could use more budget (those with 0 shares but fractional potential)
        redistributable = []
        for item in allocation:
            if item['shares'] == 0 and item['fractional_shares'] > 0:
                # Calculate how much we could allocate to this stock
                max_additional = min(unused_budget, item['fractional_allocated'] - item['allocated'])
                if max_additional > 0:
                    redistributable.append({
                        'ticker': item['ticker'],
                        'price': item['price'],
                        'max_additional': max_additional,
                        'current_allocated': item['allocated']
                    })
        
        # Redistribute unused budget to stocks that can use it
        for redist_item in sorted(redistributable, key=lambda x: x['max_additional'], reverse=True):
            if unused_budget <= 0:
                break
                
            # Calculate how much we can actually allocate
            additional_allocation = min(unused_budget, redist_item['max_additional'])
            additional_shares = int(additional_allocation // redist_item['price'])
            actual_additional = additional_shares * redist_item['price']
            
            if actual_additional > 0:
                # Update the allocation
                for item in allocation:
                    if item['ticker'] == redist_item['ticker']:
                        item['shares'] += additional_shares
                        item['allocated'] += actual_additional
                        total_allocated += actual_additional
                        unused_budget -= actual_additional
                        print(f"Debug - Redistributed ${actual_additional:.2f} to {redist_item['ticker']} (${additional_shares} shares)")
                        break
    
    # Add debug information
    print(f"Debug - Budget: ${budget}, Total Allocated: ${total_allocated:.2f}")
    print(f"Debug - Unused budget: ${budget - total_allocated:.2f}")
    for item in allocation:
        print(f"Debug - {item['ticker']}: Weight={item['weight']:.1%}, Shares={item['shares']}, Price=${item['price']:.2f}, Allocated=${item['allocated']:.2f}")
    
    return allocation


def allocate_portfolio(
    budget: float,
    tickers: List[str],
    prices: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> List[Dict]:
    """
    Legacy function for backward compatibility.
    Allocate budget across tickers based on prices and optional weights.
    Returns a list of dicts: [{ticker, price, weight, allocated, shares}]
    """
    n = len(tickers)
    if n == 0:
        return []
    if not weights:
        weights = {ticker: 1/n for ticker in tickers}
    else:
        total = sum(weights.values())
        weights = {k: v/total for k, v in weights.items()}

    allocation = []
    for ticker in tickers:
        price = prices.get(ticker)
        weight = weights.get(ticker, 0)
        allocated = budget * weight if price else 0
        shares = int(allocated // price) if price else 0
        allocation.append({
            "ticker": ticker,
            "price": price,
            "weight": weight,
            "allocated": allocated,
            "shares": shares
        })
    return allocation 


def generate_weight_recommendations(tickers: List[str], tech_preference: float = 0.6) -> Dict[str, float]:
    """
    Generate intelligent weight recommendations based on market conditions and stock characteristics.
    
    Args:
        tickers: List of stock tickers
        tech_preference: User's tech sector preference (0.0 to 1.0)
    
    Returns:
        Dict of recommended weights: {ticker: weight}
    """
    try:
        # Get stock information
        stock_info = {}
        for ticker in tickers:
            try:
                ticker_obj = yf.Ticker(ticker)
                info = ticker_obj.info
                stock_info[ticker] = {
                    'sector': info.get('sector', 'Unknown'),
                    'market_cap': info.get('marketCap', 0),
                    'beta': info.get('beta', 1.0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'dividend_yield': info.get('dividendYield', 0) or 0,
                    'price': info.get('regularMarketPrice', 0)
                }
            except Exception:
                stock_info[ticker] = {
                    'sector': 'Unknown',
                    'market_cap': 0,
                    'beta': 1.0,
                    'pe_ratio': 0,
                    'dividend_yield': 0,
                    'price': 0
                }
        
        # Calculate base weights using multiple factors
        weights = {}
        total_score = 0
        
        for ticker, info in stock_info.items():
            score = 1.0  # Base score
            
            # Factor 1: Sector preference (tech vs non-tech)
            if is_tech_stock(info['sector']):
                score *= (1 + tech_preference)  # Boost tech stocks
            else:
                score *= (1 - tech_preference * 0.5)  # Reduce non-tech stocks
            
            # Factor 2: Market cap (prefer larger, more stable companies)
            if info['market_cap'] > 100e9:  # > $100B
                score *= 1.2
            elif info['market_cap'] > 10e9:  # > $10B
                score *= 1.1
            elif info['market_cap'] < 1e9:  # < $1B
                score *= 0.8
            
            # Factor 3: Beta (prefer lower volatility)
            if info['beta'] < 0.8:
                score *= 1.1  # Low volatility
            elif info['beta'] > 1.5:
                score *= 0.9  # High volatility
            
            # Factor 4: Dividend yield (bonus for income)
            if info['dividend_yield'] > 0.02:  # > 2%
                score *= 1.05
            
            # Factor 5: P/E ratio (prefer reasonable valuations)
            if 0 < info['pe_ratio'] < 25:
                score *= 1.05
            elif info['pe_ratio'] > 50:
                score *= 0.9
            
            weights[ticker] = score
            total_score += score
        
        # Normalize weights to sum to 1.0
        if total_score > 0:
            for ticker in weights:
                weights[ticker] = weights[ticker] / total_score
        else:
            # Fallback to equal weights
            equal_weight = 1.0 / len(tickers)
            weights = {ticker: equal_weight for ticker in tickers}
        
        return weights
        
    except Exception as e:
        # Fallback to equal weights if anything goes wrong
        equal_weight = 1.0 / len(tickers)
        return {ticker: equal_weight for ticker in tickers}


def get_market_insights(tickers: List[str]) -> Dict[str, str]:
    """
    Generate market insights and recommendations for the selected stocks.
    
    Args:
        tickers: List of stock tickers
    
    Returns:
        Dict of insights: {ticker: insight}
    """
    insights = {}
    
    try:
        for ticker in tickers:
            try:
                ticker_obj = yf.Ticker(ticker)
                info = ticker_obj.info
                
                insight_parts = []
                
                # Sector analysis
                sector = info.get('sector', 'Unknown')
                if is_tech_stock(sector):
                    insight_parts.append("🖥️ Tech sector - growth potential")
                elif sector == 'Healthcare':
                    insight_parts.append("🏥 Healthcare - defensive play")
                elif sector == 'Financial Services':
                    insight_parts.append("🏦 Financial - interest rate sensitive")
                elif sector == 'Consumer Cyclical':
                    insight_parts.append("🛒 Consumer - economic cycle dependent")
                
                # Market cap analysis
                market_cap = info.get('marketCap', 0)
                if market_cap > 100e9:
                    insight_parts.append("💎 Large cap - stable")
                elif market_cap > 10e9:
                    insight_parts.append("📈 Mid cap - balanced")
                else:
                    insight_parts.append("🚀 Small cap - growth potential")
                
                # Volatility analysis
                beta = info.get('beta', 1.0)
                if beta < 0.8:
                    insight_parts.append("🛡️ Low volatility")
                elif beta > 1.5:
                    insight_parts.append("⚡ High volatility")
                
                # Dividend analysis
                dividend_yield = info.get('dividendYield', 0) or 0
                if dividend_yield > 0.03:
                    insight_parts.append("💰 High dividend")
                elif dividend_yield > 0.01:
                    insight_parts.append("💵 Moderate dividend")
                
                insights[ticker] = " | ".join(insight_parts) if insight_parts else "📊 Standard stock"
                
            except Exception:
                insights[ticker] = "📊 Limited data available"
    
    except Exception:
        for ticker in tickers:
            insights[ticker] = "📊 Data unavailable"
    
    return insights 