# 🤖 AI Stock Advisor

A comprehensive, LLM-powered investment research and portfolio management platform that combines multiple analysis methodologies for informed investment decisions.

## 🚀 Features

### 📊 **Core Analysis**
- **Stock Summaries**: Get comprehensive analysis of individual stocks
- **Market Sentiment**: AI-powered market mood detection
- **Earnings Analysis**: Track earnings surprises and performance
- **News Integration**: Real-time news sentiment analysis

### 📈 **Technical Analysis**
- **RSI (Relative Strength Index)**: Overbought/oversold detection
- **Moving Averages**: 20, 50, and 200-day moving averages
- **Bollinger Bands**: Volatility and trend analysis
- **MACD**: Momentum and trend confirmation
- **Signal Generation**: Automated buy/sell signals based on technical indicators

### 💼 **Fundamental Analysis**
- **Valuation Metrics**: P/E, P/B, EV/EBITDA ratios
- **Financial Ratios**: ROE, ROA, debt-to-equity analysis
- **Cash Flow Analysis**: Operating, investing, and financing cash flows
- **Growth Metrics**: Revenue and EPS growth analysis
- **Quality Scoring**: Comprehensive fundamental scoring system

### ⚠️ **Risk Management**
- **Position Sizing**: Kelly Criterion-based position sizing
- **Stop-Loss Logic**: Multiple stop-loss calculation methods
- **Take-Profit Rules**: Risk-reward ratio optimization
- **Correlation Analysis**: Portfolio diversification monitoring
- **Risk Metrics**: VaR, maximum drawdown, Sharpe ratio

### 📈 **Backtesting & Performance**
- **Strategy Backtesting**: Historical performance validation
- **Performance Metrics**: Sharpe ratio, win rate, profit factor
- **Strategy Comparison**: Multi-strategy performance analysis
- **Risk-Adjusted Returns**: Comprehensive performance evaluation

### 💰 **Portfolio Management**
- **Smart Allocation**: AI-powered weight recommendations
- **Sector Preferences**: Tech vs non-tech allocation
- **Budget Optimization**: Fractional share support
- **Portfolio Analysis**: Risk and correlation monitoring

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd ai_stock_advisor
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

4. **Run the application**:
```bash
streamlit run app.py
```

## 📋 Dependencies

### Core Dependencies
- `streamlit>=1.28.0`: Web application framework
- `pandas>=2.0.0`: Data manipulation
- `numpy>=1.24.0`: Numerical computing
- `yfinance>=0.2.18`: Yahoo Finance data
- `openai>=1.0.0`: OpenAI API integration

### Analysis Dependencies
- `TA-Lib>=0.4.25`: Technical analysis indicators
- `scikit-learn>=1.3.0`: Machine learning utilities
- `matplotlib>=3.7.0`: Plotting and visualization
- `seaborn>=0.12.0`: Statistical data visualization

### Additional Dependencies
- `plotly>=5.15.0`: Interactive charts
- `requests>=2.31.0`: HTTP requests
- `beautifulsoup4>=4.12.0`: Web scraping
- `fpdf>=2.7.0`: PDF report generation

## 🎯 Investment Strategies Supported

### 1. **Technical Analysis Strategies**
- **Trend Following**: Moving average crossovers
- **Mean Reversion**: RSI and Bollinger Bands
- **Momentum Trading**: MACD and price momentum
- **Breakout Trading**: Support/resistance levels

### 2. **Fundamental Analysis Strategies**
- **Value Investing**: Low P/E, high ROE screening
- **Growth Investing**: Revenue and earnings growth focus
- **Dividend Investing**: High dividend yield strategies
- **Quality Investing**: Strong financial health focus

### 3. **Quantitative Strategies**
- **Multi-Factor Models**: Combined technical and fundamental
- **Risk Parity**: Volatility-based allocation
- **Statistical Arbitrage**: Correlation-based strategies

### 4. **Risk Management**
- **Kelly Criterion**: Optimal position sizing
- **Stop-Loss Management**: Automated risk control
- **Portfolio Diversification**: Correlation monitoring
- **Dynamic Rebalancing**: Performance-based adjustments

## 🔬 Advanced Analysis Features

### Technical Analysis Module
```python
from utils.technical_analysis import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()
signals = analyzer.generate_technical_signals("AAPL")
```

### Fundamental Analysis Module
```python
from utils.fundamental_analysis import FundamentalAnalyzer

analyzer = FundamentalAnalyzer()
analysis = analyzer.analyze_fundamentals("AAPL")
```

### Risk Management Module
```python
from utils.risk_management import RiskManager

risk_manager = RiskManager(portfolio_value=10000)
position_size = risk_manager.calculate_position_size("AAPL", 150, 140)
```

### Backtesting Module
```python
from utils.backtesting import Backtester

backtester = Backtester(initial_capital=10000)
results = backtester.backtest_strategy("AAPL", strategy_params)
```

## 📊 Performance Metrics

### Technical Indicators
- **RSI**: Overbought (>70) / Oversold (<30) levels
- **Moving Averages**: Golden/Death cross detection
- **Bollinger Bands**: Volatility and trend analysis
- **MACD**: Momentum and trend confirmation

### Fundamental Metrics
- **Valuation**: P/E, P/B, EV/EBITDA ratios
- **Profitability**: ROE, ROA, gross margins
- **Financial Health**: Debt ratios, interest coverage
- **Growth**: Revenue and earnings growth rates

### Risk Metrics
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Worst historical decline
- **Value at Risk (VaR)**: Portfolio risk assessment
- **Correlation Analysis**: Diversification effectiveness

## 🎯 Decision Making Process

The AI agent combines multiple analysis methods:

1. **Market Context**: Macro mood and earnings analysis
2. **Technical Signals**: RSI, moving averages, MACD
3. **Fundamental Health**: Financial ratios and valuation
4. **Risk Assessment**: Position sizing and portfolio impact
5. **Historical Validation**: Backtesting and performance metrics

### Decision Categories
- **STRONG_BUY**: High confidence across all metrics
- **BUY**: Positive signals with moderate confidence
- **HOLD**: Mixed signals or neutral conditions
- **SELL**: Negative signals with moderate confidence
- **STRONG_SELL**: High confidence negative signals

## 🔧 Configuration

### Technical Analysis Settings
```python
# RSI parameters
rsi_period = 14
rsi_oversold = 30
rsi_overbought = 70

# Moving average periods
ma_short = 20
ma_long = 50
ma_long_term = 200
```

### Risk Management Settings
```python
# Position sizing
max_risk_per_trade = 0.02  # 2% max risk per trade
kelly_fraction_cap = 0.25  # Maximum Kelly fraction

# Stop-loss settings
stop_loss_percentage = 0.05  # 5% stop loss
atr_multiplier = 2.0        # ATR-based stop loss
```

### Backtesting Parameters
```python
# Strategy parameters
strategy_params = {
    'rsi_period': 14,
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'ma_short': 20,
    'ma_long': 50,
    'stop_loss': 0.05,
    'take_profit': 0.10
}
```

## 📈 Usage Examples

### Basic Stock Analysis
1. Navigate to "Stock Summary" tab
2. Select a trending stock or enter a ticker
3. View comprehensive analysis including:
   - Technical indicators
   - Fundamental metrics
   - AI investment decision
   - Risk assessment

### Portfolio Allocation
1. Go to "Portfolio Allocator" tab
2. Enter your budget and stock selection
3. Choose between trending stocks or custom selection
4. View AI-recommended weights and allocation
5. Analyze risk metrics and correlation

### Advanced Analysis
1. Use "Advanced Analysis" tab for detailed breakdown
2. View separate technical and fundamental analysis
3. Examine backtesting results and performance metrics
4. Compare multiple analysis methods

## ⚠️ Important Disclaimers

- **Not Financial Advice**: This tool is for educational and research purposes only
- **Past Performance**: Historical backtesting doesn't guarantee future results
- **Risk Management**: Always use proper risk management in real trading
- **Data Accuracy**: Relies on external data sources that may have delays or errors
- **Market Conditions**: Strategies may perform differently in various market conditions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
1. Check existing issues
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Built with ❤️ for informed investment decisions**
