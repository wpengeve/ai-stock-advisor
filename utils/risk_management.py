import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Position:
    """Position data structure for risk management."""
    ticker: str
    shares: int
    entry_price: float
    current_price: float
    allocation: float  # Percentage of portfolio
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class RiskManager:
    """
    Risk management module for portfolio protection and position sizing.
    """
    
    def __init__(self, portfolio_value: float, max_risk_per_trade: float = 0.02):
        self.portfolio_value = portfolio_value
        self.max_risk_per_trade = max_risk_per_trade  # 2% max risk per trade
        self.positions: List[Position] = []
    
    def calculate_position_size(self, ticker: str, entry_price: float, stop_loss: float, 
                              volatility_adjustment: float = 1.0) -> Dict[str, float]:
        """
        Calculate optimal position size using Kelly Criterion and risk management.
        
        Args:
            ticker: Stock ticker
            entry_price: Entry price
            stop_loss: Stop loss price
            volatility_adjustment: Volatility adjustment factor
        
        Returns:
            Dict with position size recommendations
        """
        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss)
        
        # Calculate maximum risk amount
        max_risk_amount = self.portfolio_value * self.max_risk_per_trade
        
        # Calculate position size based on risk
        max_shares_by_risk = max_risk_amount / risk_per_share if risk_per_share > 0 else 0
        
        # Kelly Criterion calculation (simplified)
        # Assuming 50% win rate and 1:2 risk-reward ratio
        win_rate = 0.5
        avg_win = risk_per_share * 2  # 2:1 reward-risk ratio
        avg_loss = risk_per_share
        kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        
        # Calculate Kelly-based position size
        kelly_shares = int((self.portfolio_value * kelly_fraction) / entry_price)
        
        # Apply volatility adjustment
        adjusted_shares = int(kelly_shares * volatility_adjustment)
        
        # Final position size (minimum of risk-based and Kelly-based)
        final_shares = min(max_shares_by_risk, adjusted_shares)
        
        # Calculate allocation percentage
        allocation_pct = (final_shares * entry_price) / self.portfolio_value
        
        return {
            'shares': final_shares,
            'allocation_pct': allocation_pct,
            'risk_amount': final_shares * risk_per_share,
            'kelly_fraction': kelly_fraction,
            'max_shares_by_risk': max_shares_by_risk,
            'volatility_adjustment': volatility_adjustment
        }
    
    def calculate_stop_loss(self, entry_price: float, atr_multiplier: float = 2.0, 
                           percentage_stop: float = 0.05) -> Dict[str, float]:
        """
        Calculate stop loss using multiple methods.
        
        Args:
            entry_price: Entry price
            atr_multiplier: ATR multiplier for stop loss
            percentage_stop: Percentage-based stop loss
        
        Returns:
            Dict with stop loss recommendations
        """
        # Percentage-based stop loss
        percentage_stop_price = entry_price * (1 - percentage_stop)
        
        # ATR-based stop loss (simplified)
        atr_stop_price = entry_price * (1 - (atr_multiplier * 0.02))  # Assuming 2% ATR
        
        # Support-based stop loss (simplified)
        support_stop_price = entry_price * 0.95  # 5% below entry
        
        # Choose the most conservative stop loss
        stop_loss_price = max(percentage_stop_price, atr_stop_price, support_stop_price)
        
        return {
            'stop_loss_price': stop_loss_price,
            'percentage_stop': percentage_stop_price,
            'atr_stop': atr_stop_price,
            'support_stop': support_stop_price,
            'risk_percentage': (entry_price - stop_loss_price) / entry_price
        }
    
    def calculate_take_profit(self, entry_price: float, risk_reward_ratio: float = 2.0,
                             stop_loss_price: float = None) -> Dict[str, float]:
        """
        Calculate take profit levels.
        
        Args:
            entry_price: Entry price
            risk_reward_ratio: Risk-reward ratio
            stop_loss_price: Stop loss price
        
        Returns:
            Dict with take profit recommendations
        """
        if stop_loss_price is None:
            stop_loss_price = entry_price * 0.95
        
        risk = entry_price - stop_loss_price
        reward = risk * risk_reward_ratio
        
        take_profit_price = entry_price + reward
        
        return {
            'take_profit_price': take_profit_price,
            'risk_reward_ratio': risk_reward_ratio,
            'reward_amount': reward,
            'risk_amount': risk
        }
    
    def calculate_portfolio_risk_metrics(self, positions: List[Position]) -> Dict[str, float]:
        """
        Calculate portfolio risk metrics.
        
        Args:
            positions: List of current positions
        
        Returns:
            Dict with risk metrics
        """
        if not positions:
            return {
                'total_allocation': 0,
                'portfolio_beta': 1.0,
                'max_drawdown': 0,
                'var_95': 0,
                'sharpe_ratio': 0
            }
        
        # Calculate total allocation
        total_allocation = sum(pos.allocation for pos in positions)
        
        # Calculate portfolio beta (simplified)
        portfolio_beta = sum(pos.allocation * 1.0 for pos in positions)  # Assuming beta = 1
        
        # Calculate Value at Risk (simplified)
        # Assuming normal distribution with 15% annual volatility
        daily_volatility = 0.15 / np.sqrt(252)
        var_95 = total_allocation * daily_volatility * 1.645  # 95% confidence
        
        # Calculate maximum potential drawdown
        max_drawdown = total_allocation * 0.20  # Assuming 20% max drawdown
        
        # Calculate Sharpe ratio (simplified)
        # Assuming 8% annual return and 15% volatility
        annual_return = 0.08
        annual_volatility = 0.15
        risk_free_rate = 0.02
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        
        return {
            'total_allocation': total_allocation,
            'portfolio_beta': portfolio_beta,
            'max_drawdown': max_drawdown,
            'var_95': var_95,
            'sharpe_ratio': sharpe_ratio
        }
    
    def check_correlation_risk(self, tickers: List[str], max_correlation: float = 0.7) -> Dict[str, any]:
        """
        Check correlation risk between stocks.
        
        Args:
            tickers: List of stock tickers
            max_correlation: Maximum allowed correlation
        
        Returns:
            Dict with correlation analysis
        """
        if len(tickers) < 2:
            return {"warning": "Need at least 2 stocks for correlation analysis"}
        
        try:
            # Fetch price data for correlation analysis
            price_data = {}
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="6mo")
                if not hist.empty:
                    price_data[ticker] = hist['Close']
            
            if len(price_data) < 2:
                return {"error": "Could not fetch sufficient price data"}
            
            # Create correlation matrix
            df = pd.DataFrame(price_data)
            correlation_matrix = df.corr()
            
            # Find high correlations
            high_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > max_correlation:
                        high_correlations.append({
                            'stock1': correlation_matrix.columns[i],
                            'stock2': correlation_matrix.columns[j],
                            'correlation': corr_value
                        })
            
            # Calculate average correlation
            avg_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
            
            return {
                'correlation_matrix': correlation_matrix,
                'high_correlations': high_correlations,
                'average_correlation': avg_correlation,
                'diversification_score': 1 - avg_correlation,
                'risk_level': 'HIGH' if len(high_correlations) > 0 else 'LOW'
            }
            
        except Exception as e:
            return {"error": f"Error calculating correlations: {e}"}
    
    def generate_risk_report(self, positions: List[Position], tickers: List[str]) -> Dict[str, any]:
        """
        Generate comprehensive risk report.
        
        Args:
            positions: Current positions
            tickers: All tickers in portfolio
        
        Returns:
            Dict with comprehensive risk analysis
        """
        # Portfolio risk metrics
        risk_metrics = self.calculate_portfolio_risk_metrics(positions)
        
        # Correlation analysis
        correlation_analysis = self.check_correlation_risk(tickers)
        
        # Position-level risk analysis
        position_risks = []
        for pos in positions:
            if pos.stop_loss:
                risk_amount = (pos.entry_price - pos.stop_loss) * pos.shares
                risk_pct = (pos.entry_price - pos.stop_loss) / pos.entry_price
            else:
                risk_amount = 0
                risk_pct = 0
            
            position_risks.append({
                'ticker': pos.ticker,
                'allocation': pos.allocation,
                'risk_amount': risk_amount,
                'risk_percentage': risk_pct,
                'stop_loss': pos.stop_loss,
                'take_profit': pos.take_profit
            })
        
        # Overall risk assessment
        total_risk = sum(pr['risk_amount'] for pr in position_risks)
        risk_to_portfolio = total_risk / self.portfolio_value if self.portfolio_value > 0 else 0
        
        risk_level = 'LOW'
        if risk_to_portfolio > 0.05:
            risk_level = 'HIGH'
        elif risk_to_portfolio > 0.02:
            risk_level = 'MEDIUM'
        
        return {
            'portfolio_risk_metrics': risk_metrics,
            'correlation_analysis': correlation_analysis,
            'position_risks': position_risks,
            'total_risk_amount': total_risk,
            'risk_to_portfolio_ratio': risk_to_portfolio,
            'overall_risk_level': risk_level,
            'recommendations': self._generate_risk_recommendations(risk_to_portfolio, correlation_analysis)
        }
    
    def _generate_risk_recommendations(self, risk_ratio: float, correlation_analysis: Dict) -> List[str]:
        """Generate risk management recommendations."""
        recommendations = []
        
        if risk_ratio > 0.05:
            recommendations.append("⚠️ HIGH RISK: Consider reducing position sizes or adding stop-losses")
        
        if risk_ratio > 0.02:
            recommendations.append("📊 MEDIUM RISK: Monitor positions closely and consider diversification")
        
        if correlation_analysis.get('risk_level') == 'HIGH':
            recommendations.append("🔗 HIGH CORRELATION: Consider diversifying into different sectors")
        
        if len(recommendations) == 0:
            recommendations.append("✅ Risk levels are acceptable")
        
        return recommendations 