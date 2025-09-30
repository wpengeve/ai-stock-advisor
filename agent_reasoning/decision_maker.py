import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.technical_analysis import TechnicalAnalyzer
from utils.fundamental_analysis import FundamentalAnalyzer
from utils.risk_management import RiskManager
from utils.backtesting import Backtester

def make_investment_decision(macro_mood, earnings_result, price_change, ticker=None, 
                           include_technical=True, include_fundamental=True, 
                           include_risk=True, include_backtest=True):
    """
    Enhanced AI reasoning that combines multiple analysis methods.
    """
    
    # Initialize analyzers
    technical_analyzer = TechnicalAnalyzer()
    fundamental_analyzer = FundamentalAnalyzer()
    risk_manager = RiskManager(portfolio_value=10000)  # Default portfolio value
    backtester = Backtester(initial_capital=10000)
    
    # Base confidence calculation
    confidence = 50
    
    # 1. Macro and Earnings Analysis (Original logic)
    if macro_mood == "Risk-On":
        confidence += 15
    elif macro_mood == "Risk-Off":
        confidence -= 15

    if earnings_result == "Beat":
        confidence += 10
    elif earnings_result == "Miss":
        confidence -= 10

    if price_change > 3:
        confidence += 5
    elif price_change < -3:
        confidence -= 5
    
    # 2. Technical Analysis (if enabled and ticker provided)
    technical_signals = None
    if include_technical and ticker:
        try:
            technical_signals = technical_analyzer.generate_technical_signals(ticker)
            if 'error' not in technical_signals:
                overall_signal = technical_signals.get('overall_signal', 'NEUTRAL')
                technical_confidence = technical_signals.get('confidence', 50)
                
                if overall_signal == 'BULLISH':
                    confidence += 15
                elif overall_signal == 'BEARISH':
                    confidence -= 15
                
                # Adjust confidence based on technical confidence
                confidence = (confidence + technical_confidence) / 2
        except Exception as e:
            print(f"Technical analysis error: {e}")
    
    # 3. Fundamental Analysis (if enabled and ticker provided)
    fundamental_analysis = None
    if include_fundamental and ticker:
        try:
            fundamental_analysis = fundamental_analyzer.analyze_fundamentals(ticker)
            if 'error' not in fundamental_analysis:
                fundamental_score = fundamental_analysis.get('fundamental_score', {})
                score_percentage = fundamental_score.get('score_percentage', 50)
                rating = fundamental_score.get('rating', 'FAIR')
                
                if rating == 'EXCELLENT':
                    confidence += 20
                elif rating == 'GOOD':
                    confidence += 10
                elif rating == 'FAIR':
                    confidence += 0
                else:  # POOR
                    confidence -= 15
        except Exception as e:
            print(f"Fundamental analysis error: {e}")
    
    # 4. Risk Analysis (if enabled and ticker provided)
    risk_analysis = None
    if include_risk and ticker:
        try:
            # Create a sample position for risk analysis
            from utils.risk_management import Position
            sample_position = Position(
                ticker=ticker,
                shares=100,
                entry_price=100,  # Placeholder
                current_price=100,  # Placeholder
                allocation=0.1
            )
            
            risk_report = risk_manager.generate_risk_report([sample_position], [ticker])
            risk_level = risk_report.get('overall_risk_level', 'LOW')
            
            if risk_level == 'LOW':
                confidence += 5
            elif risk_level == 'HIGH':
                confidence -= 10
        except Exception as e:
            print(f"Risk analysis error: {e}")
    
    # 5. Backtesting (if enabled and ticker provided)
    backtest_results = None
    if include_backtest and ticker:
        try:
            # Define a simple strategy for backtesting
            strategy_params = {
                'rsi_period': 14,
                'rsi_oversold': 30,
                'rsi_overbought': 70,
                'ma_short': 20,
                'ma_long': 50,
                'stop_loss': 0.05,
                'take_profit': 0.10
            }
            
            backtest_results = backtester.backtest_strategy(ticker, strategy_params)
            if 'error' not in backtest_results:
                performance_metrics = backtest_results.get('performance_metrics', {})
                sharpe_ratio = performance_metrics.get('sharpe_ratio', 0)
                total_return = performance_metrics.get('total_return', 0)
                
                if sharpe_ratio > 1.0:
                    confidence += 10
                elif sharpe_ratio > 0.5:
                    confidence += 5
                elif sharpe_ratio < 0:
                    confidence -= 5
                
                if total_return > 0.1:  # 10% return
                    confidence += 5
                elif total_return < -0.1:  # -10% return
                    confidence -= 5
        except Exception as e:
            print(f"Backtesting error: {e}")
    
    # Final decision logic
    if confidence >= 75:
        decision = "STRONG_BUY"
    elif confidence >= 60:
        decision = "BUY"
    elif confidence >= 40:
        decision = "HOLD"
    elif confidence >= 25:
        decision = "SELL"
    else:
        decision = "STRONG_SELL"
    
    # Ensure confidence stays within bounds
    confidence = max(0, min(100, confidence))
    
    # Generate comprehensive explanation
    explanation = generate_comprehensive_explanation(
        macro_mood, earnings_result, price_change, technical_signals, 
        fundamental_analysis, risk_analysis, backtest_results, decision, confidence
    )
    
    return decision, confidence, explanation

def generate_comprehensive_explanation(macro_mood, earnings_result, price_change, 
                                     technical_signals, fundamental_analysis, 
                                     risk_analysis, backtest_results, decision, confidence):
    """
    Generate a comprehensive explanation of the investment decision.
    """
    
    explanation = f"""
### 🤖 Enhanced AI Investment Decision

**Final Decision: {decision}**  
**Confidence: {confidence}%**

---

### 📊 Analysis Summary

#### 🎯 **Market Context**
- **Macro Mood**: {macro_mood}
- **Earnings Result**: {earnings_result}
- **5-Day Price Change**: {price_change:.2f}%
"""
    
    # Technical Analysis Section
    if technical_signals and 'error' not in technical_signals:
        explanation += f"""
#### 📈 **Technical Analysis**
- **Overall Signal**: {technical_signals.get('overall_signal', 'NEUTRAL')}
- **RSI**: {technical_signals.get('rsi', 0):.1f} ({technical_signals.get('rsi_signal', {}).get('action', 'HOLD')})
- **Technical Confidence**: {technical_signals.get('confidence', 0)}%
- **Bullish Signals**: {technical_signals.get('bullish_signals', 0)} / {technical_signals.get('total_signals', 0)}
- **Bearish Signals**: {technical_signals.get('bearish_signals', 0)} / {technical_signals.get('total_signals', 0)}
"""
    
    # Fundamental Analysis Section
    if fundamental_analysis and 'error' not in fundamental_analysis:
        fundamental_score = fundamental_analysis.get('fundamental_score', {})
        recommendation = fundamental_analysis.get('recommendation', {})
        
        explanation += f"""
#### 💼 **Fundamental Analysis**
- **Fundamental Score**: {fundamental_score.get('score_percentage', 0):.1f}%
- **Rating**: {fundamental_score.get('rating', 'N/A')}
- **Recommendation**: {recommendation.get('recommendation', 'N/A')}
- **P/E Ratio**: {fundamental_analysis.get('valuation_metrics', {}).get('pe_ratio', 0):.2f}
- **ROE**: {fundamental_analysis.get('financial_ratios', {}).get('roe', 0):.2%}
- **Debt/Equity**: {fundamental_analysis.get('debt_analysis', {}).get('debt_to_equity', 0):.2f}
"""
    
    # Risk Analysis Section
    if risk_analysis:
        explanation += f"""
#### ⚠️ **Risk Analysis**
- **Risk Level**: {risk_analysis.get('overall_risk_level', 'N/A')}
- **Risk to Portfolio**: {risk_analysis.get('risk_to_portfolio_ratio', 0):.2%}
- **Total Risk Amount**: ${risk_analysis.get('total_risk_amount', 0):,.2f}
"""
    
    # Backtesting Section
    if backtest_results and 'error' not in backtest_results:
        performance_metrics = backtest_results.get('performance_metrics', {})
        explanation += f"""
#### 📈 **Strategy Backtesting**
- **Total Return**: {performance_metrics.get('total_return', 0):.2%}
- **Sharpe Ratio**: {performance_metrics.get('sharpe_ratio', 0):.2f}
- **Max Drawdown**: {performance_metrics.get('max_drawdown', 0):.2%}
- **Win Rate**: {performance_metrics.get('win_rate', 0):.2%}
- **Total Trades**: {performance_metrics.get('total_trades', 0)}
"""
    
    # Final recommendation
    explanation += f"""
---

### 🎯 **Investment Recommendation**

**Action**: {decision}

**Reasoning**: This recommendation is based on a comprehensive analysis combining:
- Market sentiment and earnings performance
- Technical indicators and price patterns
- Fundamental financial health and valuation
- Risk assessment and portfolio impact
- Historical strategy performance

**Confidence Level**: {confidence}% - {'High confidence' if confidence >= 70 else 'Moderate confidence' if confidence >= 50 else 'Low confidence'}
"""
    
    return explanation.strip()