"""
Market Configuration for Multi-Market Support
"""

# Market configurations
MARKET_CONFIGS = {
    "US": {
        "name": "🇺🇸 US Stock Market",
        "currency": "USD",
        "currency_symbol": "$",
        "suffix": "",
        "data_source": "yahoo",
        "trading_hours": "9:30 AM - 4:00 PM EST",
        "timezone": "America/New_York",
        "popular_stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "AMD", "INTC"],
        "sectors": ["Technology", "Healthcare", "Financial", "Consumer", "Industrial", "Energy", "Materials", "Utilities", "Real Estate", "Communication"]
    },
    "TW": {
        "name": "🇹🇼 Taiwan Stock Market",
        "currency": "TWD",
        "currency_symbol": "NT$",
        "suffix": ".TW",
        "data_source": "yahoo",
        "trading_hours": "9:00 AM - 1:30 PM CST",
        "timezone": "Asia/Taipei",
        "popular_stocks": ["2330.TW", "2317.TW", "2454.TW", "2382.TW", "6505.TW", "2881.TW", "2882.TW", "2891.TW", "1102.TW", "2002.TW"],
        "stock_names": {
            "2330.TW": "台積電 (TSMC)",
            "2317.TW": "鴻海 (Hon Hai)",
            "2454.TW": "聯發科 (MediaTek)",
            "2382.TW": "廣達 (Quanta)",
            "6505.TW": "台塑 (Formosa Plastics)",
            "2881.TW": "富邦金 (Fubon Financial)",
            "2882.TW": "國泰金 (Cathay Financial)",
            "2891.TW": "中信金 (CTBC Financial)",
            "1102.TW": "亞泥 (Asia Cement)",
            "2002.TW": "中鋼 (China Steel)"
        },
        "sectors": ["Semiconductors", "Technology", "Financial", "Traditional Industries", "Biotech", "Energy", "Materials", "Utilities", "Real Estate", "Communication"]
    }
    # Commented out other markets for now - keeping only US and Taiwan
    # "HK": {
    #     "name": "🇭🇰 Hong Kong Stock Market",
    #     "currency": "HKD",
    #     "currency_symbol": "HK$",
    #     "suffix": ".HK",
    #     "data_source": "yahoo",
    #     "trading_hours": "9:30 AM - 4:00 PM HKT",
    #     "timezone": "Asia/Hong_Kong",
    #     "popular_stocks": ["0700.HK", "0941.HK", "1299.HK", "1398.HK", "3988.HK", "2318.HK", "2628.HK", "0939.HK", "0388.HK", "3690.HK"],
    #     "stock_names": {
    #         "0700.HK": "騰訊 (Tencent)",
    #         "0941.HK": "中國移動 (China Mobile)",
    #         "1299.HK": "友邦保險 (AIA)",
    #         "1398.HK": "工商銀行 (ICBC)",
    #         "3988.HK": "中國銀行 (Bank of China)",
    #         "2318.HK": "平安保險 (Ping An)",
    #         "2628.HK": "中國人壽 (China Life)",
    #         "0939.HK": "建設銀行 (CCB)",
    #         "0388.HK": "香港交易所 (HKEX)",
    #         "3690.HK": "美團 (Meituan)"
    #     },
    #     "sectors": ["Technology", "Financial", "Real Estate", "Energy", "Utilities", "Consumer", "Healthcare", "Materials", "Industrial", "Communication"]
    # },
    # "JP": {
    #     "name": "🇯🇵 Japan Stock Market",
    #     "currency": "JPY",
    #     "currency_symbol": "¥",
    #     "suffix": ".T",
    #     "data_source": "yahoo",
    #     "trading_hours": "9:00 AM - 3:00 PM JST",
    #     "timezone": "Asia/Tokyo",
    #     "popular_stocks": ["6758.T", "7203.T", "9984.T", "6861.T", "7974.T", "8316.T", "9432.T", "4063.T", "8035.T", "4519.T"],
    #     "sectors": ["Technology", "Automotive", "Financial", "Consumer", "Industrial", "Healthcare", "Materials", "Utilities", "Real Estate", "Communication"]
    # },
    # "CN": {
    #     "name": "🇨🇳 China Stock Market",
    #     "currency": "CNY",
    #     "currency_symbol": "¥",
    #     "suffix": ".SS",  # Shanghai Stock Exchange
    #     "data_source": "yahoo",
    #     "trading_hours": "9:30 AM - 3:00 PM CST",
    #     "timezone": "Asia/Shanghai",
    #     "popular_stocks": ["600036.SS", "600519.SS", "000858.SZ", "002415.SZ", "300059.SZ", "600276.SS", "000725.SZ", "002594.SZ", "600887.SS", "000001.SZ"],
    #     "stock_names": {
    #         "600036.SS": "招商銀行 (China Merchants Bank)",
    #         "600519.SS": "貴州茅台 (Kweichow Moutai)",
    #         "000858.SZ": "五糧液 (Wuliangye)",
    #         "002415.SZ": "海康威視 (Hikvision)",
    #         "300059.SZ": "東方財富 (East Money)",
    #         "600276.SS": "恒瑞醫藥 (Jiangsu Hengrui)",
    #         "000725.SZ": "京東方 (BOE Technology)",
    #         "002594.SZ": "比亞迪 (BYD)",
    #         "600887.SS": "伊利股份 (Inner Mongolia Yili)",
    #         "000001.SZ": "平安銀行 (Ping An Bank)"
    #     },
    #     "sectors": ["Technology", "Financial", "Consumer", "Industrial", "Healthcare", "Energy", "Materials", "Utilities", "Real Estate", "Communication"]
    # },
    # "KR": {
    #     "name": "🇰🇷 South Korea Stock Market",
    #     "currency": "KRW",
    #     "currency_symbol": "₩",
    #     "suffix": ".KS",
    #     "data_source": "yahoo",
    #     "trading_hours": "9:00 AM - 3:30 PM KST",
    #     "timezone": "Asia/Seoul",
    #     "popular_stocks": ["005930.KS", "000660.KS", "035420.KS", "207940.KS", "006400.KS", "035720.KS", "051910.KS", "068270.KS", "012330.KS", "000270.KS"],
    #     "sectors": ["Technology", "Automotive", "Financial", "Consumer", "Industrial", "Healthcare", "Materials", "Utilities", "Real Estate", "Communication"]
    # },
    # "SG": {
    #     "name": "🇸🇬 Singapore Stock Market",
    #     "currency": "SGD",
    #     "currency_symbol": "S$",
    #     "suffix": ".SI",
    #     "data_source": "yahoo",
    #     "trading_hours": "9:00 AM - 5:00 PM SGT",
    #     "timezone": "Asia/Singapore",
    #     "popular_stocks": ["D05.SI", "U11.SI", "O39.SI", "C6L.SI", "H78.SI", "C38U.SI", "BN4.SI", "F34.SI", "G13.SI", "V03.SI"],
    #     "sectors": ["Banking", "Real Estate", "Technology", "Consumer", "Industrial", "Healthcare", "Energy", "Materials", "Utilities", "Communication"]
    # }
}

# Company name to ticker mapping for different markets
MARKET_COMPANY_MAPPINGS = {
    "US": {
        'APPLE': 'AAPL',
        'MICROSOFT': 'MSFT', 
        'GOOGLE': 'GOOGL',
        'ALPHABET': 'GOOGL',
        'AMAZON': 'AMZN',
        'TESLA': 'TSLA',
        'META': 'META',
        'FACEBOOK': 'META',
        'NETFLIX': 'NFLX',
        'NVIDIA': 'NVDA',
        'TARGET': 'TGT',
        'WALMART': 'WMT',
        'COSTCO': 'COST',
        'HOME DEPOT': 'HD',
        'LOWES': 'LOW',
        'BOEING': 'BA',
        'JOHNSON & JOHNSON': 'JNJ',
        'JPMORGAN': 'JPM',
        'JPMORGAN CHASE': 'JPM',
        'BANK OF AMERICA': 'BAC',
        'WELLS FARGO': 'WFC',
        'GOLDMAN SACHS': 'GS',
        'MORGAN STANLEY': 'MS',
        'VISA': 'V',
        'MASTERCARD': 'MA',
        'PAYPAL': 'PYPL',
        'SQUARE': 'SQ',
        'UBER': 'UBER',
        'LYFT': 'LYFT',
        'AIRBNB': 'ABNB',
        'ZOOM': 'ZM',
        'SLACK': 'WORK',
        'SALESFORCE': 'CRM',
        'ADOBE': 'ADBE',
        'INTEL': 'INTC',
        'AMD': 'AMD',
        'CISCO': 'CSCO',
        'IBM': 'IBM',
        'ORACLE': 'ORCL',
        'SAP': 'SAP',
        'TWITTER': 'TWTR',
        'SNAPCHAT': 'SNAP',
        'PINTEREST': 'PINS',
        'SPOTIFY': 'SPOT',
        'PELOTON': 'PTON',
        'ROBINHOOD': 'HOOD',
        'COINBASE': 'COIN',
        'DOORDASH': 'DASH',
        'SNOWFLAKE': 'SNOW',
        'PALANTIR': 'PLTR',
        'CROWDSTRIKE': 'CRWD',
        'ZSCALER': 'ZS',
        'OKTA': 'OKTA',
        'TWILIO': 'TWLO',
        'SHOPIFY': 'SHOP',
        'SQUARE': 'SQ',
        'STRIPE': 'STRIPE',
        'PLAID': 'PLAID'
    },
    "TW": {
        'TSMC': '2330.TW',
        'HON HAI': '2317.TW',
        'MEDIATEK': '2454.TW',
        'QUANTA': '2382.TW',
        'FORMOSA PLASTICS': '6505.TW',
        'FUBON': '2881.TW',
        'CHINATRUST': '2882.TW',
        'CATHAY': '2891.TW',
        'ASUSTEK': '2357.TW',
        'ACER': '2353.TW',
        'DELTA': '2308.TW',
        'LITEON': '2301.TW',
        'UNIMICRON': '3037.TW',
        'INVENTEC': '2356.TW',
        'COMPAL': '2324.TW'
    }
    # Commented out other market mappings for now
    # "HK": {
    #     'TENCENT': '0700.HK',
    #     'CHINA MOBILE': '0941.HK',
    #     'AIA': '1299.HK',
    #     'ICBC': '1398.HK',
    #     'CCB': '3988.HK',
    #     'PING AN': '2318.HK',
    #     'CHINA LIFE': '2628.HK',
    #     'CCB': '0939.HK',
    #     'HKEX': '0388.HK',
    #     'MEITUAN': '3690.HK',
    #     'JD': '9618.HK',
    #     'NETEASE': '9999.HK',
    #     'BABA': '9988.HK',
    #     'BAIDU': '9888.HK',
    #     'XIAOMI': '1810.HK'
    # }
}

def get_market_config(market_code):
    """Get configuration for a specific market"""
    return MARKET_CONFIGS.get(market_code, MARKET_CONFIGS["US"])

def get_market_companies(market_code):
    """Get company mappings for a specific market"""
    return MARKET_COMPANY_MAPPINGS.get(market_code, MARKET_COMPANY_MAPPINGS["US"])

def format_ticker(ticker, market_code):
    """Format ticker with market suffix if needed"""
    config = get_market_config(market_code)
    suffix = config.get("suffix", "")
    
    if suffix and not ticker.endswith(suffix):
        return f"{ticker}{suffix}"
    return ticker

def format_currency(amount, market_code):
    """Format amount with market currency"""
    config = get_market_config(market_code)
    currency_symbol = config.get("currency_symbol", "$")
    currency = config.get("currency", "USD")
    
    if isinstance(amount, (int, float)):
        return f"{currency_symbol}{amount:,.2f}"
    return f"{currency_symbol}{amount}"

def get_popular_stocks(market_code):
    """Get popular stocks for a market"""
    config = get_market_config(market_code)
    return config.get("popular_stocks", [])

def get_market_sectors(market_code):
    """Get sectors for a market"""
    config = get_market_config(market_code)
    return config.get("sectors", [])

def get_stock_name(ticker, market_code):
    """Get formatted stock name with Mandarin and English"""
    config = get_market_config(market_code)
    stock_names = config.get("stock_names", {})
    
    # If we have a specific name mapping, use it
    if ticker in stock_names:
        return stock_names[ticker]
    
    # Otherwise, return just the ticker
    return ticker
