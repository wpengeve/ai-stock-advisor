import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("Matplotlib/Seaborn not available, plotting features disabled")

class Backtester:
    """
    Backtesting module for strategy validation and performance analysis.
    """
    
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.results = {}
    
    def backtest_strategy(self, ticker: str, strategy_params: Dict, 
                         start_date: str = None, end_date: str = None) -> Dict[str, any]:
        """
        Backtest a trading strategy on historical data.
        
        Args:
            ticker: Stock ticker
            strategy_params: Strategy parameters
            start_date: Start date for backtest
            end_date: End date for backtest
        
        Returns:
            Dict with backtest results and performance metrics
        """
        # Fetch historical data
        stock = yf.Ticker(ticker)
        
        if start_date and end_date:
            hist = stock.history(start=start_date, end=end_date)
        else:
            hist = stock.history(period="2y")  # Default to 2 years
        
        if hist.empty:
            return {"error": f"Could not fetch data for {ticker}"}
        
        # Initialize backtest variables
        capital = self.initial_capital
        shares = 0
        trades = []
        equity_curve = []
        
        # Strategy parameters
        rsi_period = strategy_params.get('rsi_period', 14)
        rsi_oversold = strategy_params.get('rsi_oversold', 30)
        rsi_overbought = strategy_params.get('rsi_overbought', 70)
        ma_short = strategy_params.get('ma_short', 20)
        ma_long = strategy_params.get('ma_long', 50)
        stop_loss = strategy_params.get('stop_loss', 0.05)
        take_profit = strategy_params.get('take_profit', 0.10)
        
        # Calculate indicators
        hist['RSI'] = self._calculate_rsi(hist['Close'], rsi_period)
        hist['MA_Short'] = hist['Close'].rolling(window=ma_short).mean()
        hist['MA_Long'] = hist['Close'].rolling(window=ma_long).mean()
        
        # Run backtest
        for i in range(len(hist)):
            current_price = hist['Close'].iloc[i]
            current_rsi = hist['RSI'].iloc[i]
            current_ma_short = hist['MA_Short'].iloc[i]
            current_ma_long = hist['MA_Long'].iloc[i]
            
            # Skip if indicators are not available
            if pd.isna(current_rsi) or pd.isna(current_ma_short) or pd.isna(current_ma_long):
                equity_curve.append(capital + (shares * current_price))
                continue
            
            # Generate signals
            signal = self._generate_signal(current_rsi, current_ma_short, current_ma_long, 
                                        rsi_oversold, rsi_overbought)
            
            # Execute trades
            if signal == 'BUY' and shares == 0:
                # Buy signal
                shares = capital // current_price
                capital -= shares * current_price
                entry_price = current_price
                trades.append({
                    'date': hist.index[i],
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares,
                    'capital': capital
                })
            
            elif signal == 'SELL' and shares > 0:
                # Sell signal
                capital += shares * current_price
                trades.append({
                    'date': hist.index[i],
                    'action': 'SELL',
                    'price': current_price,
                    'shares': shares,
                    'capital': capital
                })
                shares = 0
            
            # Check stop loss and take profit
            if shares > 0:
                price_change = (current_price - entry_price) / entry_price
                
                if price_change <= -stop_loss:  # Stop loss hit
                    capital += shares * current_price
                    trades.append({
                        'date': hist.index[i],
                        'action': 'STOP_LOSS',
                        'price': current_price,
                        'shares': shares,
                        'capital': capital
                    })
                    shares = 0
                
                elif price_change >= take_profit:  # Take profit hit
                    capital += shares * current_price
                    trades.append({
                        'date': hist.index[i],
                        'action': 'TAKE_PROFIT',
                        'price': current_price,
                        'shares': shares,
                        'capital': capital
                    })
                    shares = 0
            
            # Record equity
            equity_curve.append(capital + (shares * current_price))
        
        # Close any remaining position
        if shares > 0:
            final_price = hist['Close'].iloc[-1]
            capital += shares * final_price
            trades.append({
                'date': hist.index[-1],
                'action': 'CLOSE',
                'price': final_price,
                'shares': shares,
                'capital': capital
            })
        
        # Calculate performance metrics
        final_capital = equity_curve[-1]
        performance_metrics = self._calculate_performance_metrics(equity_curve, trades, hist)
        
        return {
            'ticker': ticker,
            'initial_capital': self.initial_capital,
            'final_capital': final_capital,
            'total_return': (final_capital - self.initial_capital) / self.initial_capital,
            'trades': trades,
            'equity_curve': equity_curve,
            'performance_metrics': performance_metrics,
            'strategy_params': strategy_params
        }
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _generate_signal(self, rsi: float, ma_short: float, ma_long: float,
                        rsi_oversold: float, rsi_overbought: float) -> str:
        """Generate trading signal based on indicators."""
        # RSI signals
        rsi_buy = rsi < rsi_oversold
        rsi_sell = rsi > rsi_overbought
        
        # Moving average signals
        ma_buy = ma_short > ma_long
        ma_sell = ma_short < ma_long
        
        # Combined signal
        if rsi_buy and ma_buy:
            return 'BUY'
        elif rsi_sell or ma_sell:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _calculate_performance_metrics(self, equity_curve: List[float], 
                                     trades: List[Dict], hist: pd.DataFrame) -> Dict[str, float]:
        """Calculate comprehensive performance metrics."""
        equity_series = pd.Series(equity_curve)
        
        # Basic metrics
        total_return = (equity_series.iloc[-1] - equity_series.iloc[0]) / equity_series.iloc[0]
        
        # Calculate daily returns
        daily_returns = equity_series.pct_change().dropna()
        
        # Risk metrics
        volatility = daily_returns.std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (daily_returns.mean() * 252) / volatility if volatility > 0 else 0
        
        # Maximum drawdown
        cumulative_returns = (1 + daily_returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Trade analysis
        if trades:
            winning_trades = [t for t in trades if t['action'] in ['SELL', 'TAKE_PROFIT']]
            losing_trades = [t for t in trades if t['action'] == 'STOP_LOSS']
            
            win_rate = len(winning_trades) / len(trades) if trades else 0
            
            # Calculate average win/loss
            if winning_trades and losing_trades:
                avg_win = np.mean([t['price'] for t in winning_trades])
                avg_loss = np.mean([t['price'] for t in losing_trades])
                profit_factor = avg_win / avg_loss if avg_loss > 0 else float('inf')
            else:
                profit_factor = 0
        else:
            win_rate = 0
            profit_factor = 0
        
        # Buy and hold comparison
        buy_hold_return = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]
        excess_return = total_return - buy_hold_return
        
        return {
            'total_return': total_return,
            'annualized_return': total_return * (252 / len(equity_series)),
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': len(trades),
            'buy_hold_return': buy_hold_return,
            'excess_return': excess_return
        }
    
    def compare_strategies(self, ticker: str, strategies: Dict[str, Dict]) -> Dict[str, any]:
        """
        Compare multiple strategies on the same stock.
        
        Args:
            ticker: Stock ticker
            strategies: Dict of strategy names and parameters
        
        Returns:
            Dict with comparison results
        """
        results = {}
        
        for strategy_name, strategy_params in strategies.items():
            result = self.backtest_strategy(ticker, strategy_params)
            if 'error' not in result:
                results[strategy_name] = result
        
        # Create comparison table
        comparison_data = []
        for strategy_name, result in results.items():
            metrics = result['performance_metrics']
            comparison_data.append({
                'Strategy': strategy_name,
                'Total Return': f"{metrics['total_return']:.2%}",
                'Sharpe Ratio': f"{metrics['sharpe_ratio']:.2f}",
                'Max Drawdown': f"{metrics['max_drawdown']:.2%}",
                'Win Rate': f"{metrics['win_rate']:.2%}",
                'Total Trades': metrics['total_trades']
            })
        
        return {
            'comparison_table': pd.DataFrame(comparison_data),
            'detailed_results': results
        }
    
    def generate_performance_report(self, backtest_result: Dict) -> str:
        """Generate a human-readable performance report."""
        if 'error' in backtest_result:
            return f"❌ Error: {backtest_result['error']}"
        
        metrics = backtest_result['performance_metrics']
        
        report = f"""
## 📊 Backtest Results for {backtest_result['ticker']}

### 💰 Returns
- **Total Return**: {metrics['total_return']:.2%}
- **Annualized Return**: {metrics['annualized_return']:.2%}
- **Buy & Hold Return**: {metrics['buy_hold_return']:.2%}
- **Excess Return**: {metrics['excess_return']:.2%}

### 📈 Risk Metrics
- **Volatility**: {metrics['volatility']:.2%}
- **Sharpe Ratio**: {metrics['sharpe_ratio']:.2f}
- **Maximum Drawdown**: {metrics['max_drawdown']:.2%}

### 🎯 Trading Performance
- **Total Trades**: {metrics['total_trades']}
- **Win Rate**: {metrics['win_rate']:.2%}
- **Profit Factor**: {metrics['profit_factor']:.2f}

### 📋 Strategy Parameters
"""
        
        for key, value in backtest_result['strategy_params'].items():
            report += f"- **{key}**: {value}\n"
        
        return report 