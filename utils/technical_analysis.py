import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, Tuple, Optional
try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    print("TA-Lib not available, using fallback implementations")

class TechnicalAnalyzer:
    """
    Technical analysis module for stock price analysis and signal generation.
    """
    
    def __init__(self, period: int = 14):
        self.period = period
    
    def get_stock_data(self, ticker: str, period: str = "6mo") -> pd.DataFrame:
        """
        Fetch stock data for technical analysis.
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (e.g., "6mo", "1y", "2y")
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            prices: Price series
            period: RSI period (default 14)
        
        Returns:
            RSI values
        """
        if TALIB_AVAILABLE:
            try:
                rsi = talib.RSI(prices.values, timeperiod=period)
                return pd.Series(rsi, index=prices.index)
            except:
                pass
        
        # Fallback calculation
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_moving_averages(self, prices: pd.Series) -> Dict[str, pd.Series]:
        """
        Calculate various moving averages.
        
        Args:
            prices: Price series
        
        Returns:
            Dict with different MA values
        """
        if TALIB_AVAILABLE:
            try:
                ma_20 = talib.SMA(prices.values, timeperiod=20)
                ma_50 = talib.SMA(prices.values, timeperiod=50)
                ma_200 = talib.SMA(prices.values, timeperiod=200)
                
                return {
                    'MA_20': pd.Series(ma_20, index=prices.index),
                    'MA_50': pd.Series(ma_50, index=prices.index),
                    'MA_200': pd.Series(ma_200, index=prices.index)
                }
            except:
                pass
        
        # Fallback calculation
        return {
            'MA_20': prices.rolling(window=20).mean(),
            'MA_50': prices.rolling(window=50).mean(),
            'MA_200': prices.rolling(window=200).mean()
        }
    
    def calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands.
        
        Args:
            prices: Price series
            period: MA period (default 20)
            std_dev: Standard deviation multiplier (default 2)
        
        Returns:
            Dict with upper, middle, and lower bands
        """
        if TALIB_AVAILABLE:
            try:
                upper, middle, lower = talib.BBANDS(prices.values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
                
                return {
                    'BB_Upper': pd.Series(upper, index=prices.index),
                    'BB_Middle': pd.Series(middle, index=prices.index),
                    'BB_Lower': pd.Series(lower, index=prices.index)
                }
            except:
                pass
        
        # Fallback calculation
        ma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        return {
            'BB_Upper': ma + (std * std_dev),
            'BB_Middle': ma,
            'BB_Lower': ma - (std * std_dev)
        }
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            prices: Price series
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        
        Returns:
            Dict with MACD line, signal line, and histogram
        """
        if TALIB_AVAILABLE:
            try:
                macd, signal_line, histogram = talib.MACD(prices.values, fastperiod=fast, slowperiod=slow, signalperiod=signal)
                
                return {
                    'MACD': pd.Series(macd, index=prices.index),
                    'Signal': pd.Series(signal_line, index=prices.index),
                    'Histogram': pd.Series(histogram, index=prices.index)
                }
            except:
                pass
        
        # Fallback calculation
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return {
            'MACD': macd_line,
            'Signal': signal_line,
            'Histogram': histogram
        }
    
    def generate_technical_signals(self, ticker: str) -> Dict[str, any]:
        """
        Generate comprehensive technical analysis signals for a stock.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dict with technical signals and analysis
        """
        data = self.get_stock_data(ticker)
        if data.empty:
            return {"error": f"Could not fetch data for {ticker}"}
        
        close_prices = data['Close']
        
        # Calculate all indicators
        rsi = self.calculate_rsi(close_prices)
        moving_averages = self.calculate_moving_averages(close_prices)
        bollinger_bands = self.calculate_bollinger_bands(close_prices)
        macd_data = self.calculate_macd(close_prices)
        
        # Get latest values
        current_price = close_prices.iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_ma_20 = moving_averages['MA_20'].iloc[-1]
        current_ma_50 = moving_averages['MA_50'].iloc[-1]
        current_ma_200 = moving_averages['MA_200'].iloc[-1]
        current_bb_upper = bollinger_bands['BB_Upper'].iloc[-1]
        current_bb_lower = bollinger_bands['BB_Lower'].iloc[-1]
        current_macd = macd_data['MACD'].iloc[-1]
        current_signal = macd_data['Signal'].iloc[-1]
        
        # Generate signals
        signals = {
            'ticker': ticker,
            'current_price': current_price,
            'rsi': current_rsi,
            'rsi_signal': self._interpret_rsi(current_rsi),
            'ma_signals': self._interpret_moving_averages(current_price, current_ma_20, current_ma_50, current_ma_200),
            'bollinger_signals': self._interpret_bollinger_bands(current_price, current_bb_upper, current_bb_lower),
            'macd_signals': self._interpret_macd(current_macd, current_signal),
            'overall_signal': 'NEUTRAL',
            'confidence': 50
        }
        
        # Calculate overall signal and confidence
        signals.update(self._calculate_overall_signal(signals))
        
        return signals
    
    def _interpret_rsi(self, rsi: float) -> Dict[str, any]:
        """Interpret RSI values."""
        if rsi > 70:
            return {"signal": "OVERBOUGHT", "strength": "STRONG", "action": "SELL"}
        elif rsi > 60:
            return {"signal": "OVERBOUGHT", "strength": "WEAK", "action": "CAUTION"}
        elif rsi < 30:
            return {"signal": "OVERSOLD", "strength": "STRONG", "action": "BUY"}
        elif rsi < 40:
            return {"signal": "OVERSOLD", "strength": "WEAK", "action": "WATCH"}
        else:
            return {"signal": "NEUTRAL", "strength": "NEUTRAL", "action": "HOLD"}
    
    def _interpret_moving_averages(self, price: float, ma_20: float, ma_50: float, ma_200: float) -> Dict[str, any]:
        """Interpret moving average signals."""
        signals = []
        
        # Price vs MA signals
        if price > ma_20:
            signals.append({"type": "PRICE_ABOVE_MA20", "signal": "BULLISH"})
        else:
            signals.append({"type": "PRICE_BELOW_MA20", "signal": "BEARISH"})
        
        if price > ma_50:
            signals.append({"type": "PRICE_ABOVE_MA50", "signal": "BULLISH"})
        else:
            signals.append({"type": "PRICE_BELOW_MA50", "signal": "BEARISH"})
        
        if price > ma_200:
            signals.append({"type": "PRICE_ABOVE_MA200", "signal": "BULLISH"})
        else:
            signals.append({"type": "PRICE_BELOW_MA200", "signal": "BEARISH"})
        
        # Golden/Death Cross
        if ma_20 > ma_50:
            signals.append({"type": "GOLDEN_CROSS_20_50", "signal": "BULLISH"})
        else:
            signals.append({"type": "DEATH_CROSS_20_50", "signal": "BEARISH"})
        
        return {"signals": signals}
    
    def _interpret_bollinger_bands(self, price: float, upper: float, lower: float) -> Dict[str, any]:
        """Interpret Bollinger Bands signals."""
        if price > upper:
            return {"signal": "OVERBOUGHT", "action": "SELL"}
        elif price < lower:
            return {"signal": "OVERSOLD", "action": "BUY"}
        else:
            return {"signal": "NEUTRAL", "action": "HOLD"}
    
    def _interpret_macd(self, macd: float, signal: float) -> Dict[str, any]:
        """Interpret MACD signals."""
        if macd > signal:
            return {"signal": "BULLISH", "strength": "STRONG" if macd > 0 else "WEAK"}
        else:
            return {"signal": "BEARISH", "strength": "STRONG" if macd < 0 else "WEAK"}
    
    def _calculate_overall_signal(self, signals: Dict) -> Dict[str, any]:
        """Calculate overall technical signal and confidence."""
        bullish_count = 0
        bearish_count = 0
        total_signals = 0
        
        # Count signals
        if signals['rsi_signal']['action'] == 'BUY':
            bullish_count += 1
        elif signals['rsi_signal']['action'] == 'SELL':
            bearish_count += 1
        total_signals += 1
        
        # MA signals
        for ma_signal in signals['ma_signals']['signals']:
            if ma_signal['signal'] == 'BULLISH':
                bullish_count += 1
            elif ma_signal['signal'] == 'BEARISH':
                bearish_count += 1
            total_signals += 1
        
        # Bollinger Bands
        if signals['bollinger_signals']['action'] == 'BUY':
            bullish_count += 1
        elif signals['bollinger_signals']['action'] == 'SELL':
            bearish_count += 1
        total_signals += 1
        
        # MACD
        if signals['macd_signals']['signal'] == 'BULLISH':
            bullish_count += 1
        elif signals['macd_signals']['signal'] == 'BEARISH':
            bearish_count += 1
        total_signals += 1
        
        # Calculate overall signal
        if bullish_count > bearish_count:
            overall_signal = "BULLISH"
            confidence = min(90, 50 + (bullish_count - bearish_count) * 10)
        elif bearish_count > bullish_count:
            overall_signal = "BEARISH"
            confidence = min(90, 50 + (bearish_count - bullish_count) * 10)
        else:
            overall_signal = "NEUTRAL"
            confidence = 50
        
        return {
            "overall_signal": overall_signal,
            "confidence": confidence,
            "bullish_signals": bullish_count,
            "bearish_signals": bearish_count,
            "total_signals": total_signals
        } 