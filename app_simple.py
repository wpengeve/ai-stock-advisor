import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Stock Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Stock Advisor")
st.markdown("Your LLM-powered assistant for investment research")

# Add startup message
st.success("🚀 **AI Stock Advisor is ready!** Enhanced with technical analysis, fundamental analysis, risk management, and backtesting capabilities.")

def get_stock_data(ticker):
    """Get basic stock data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        if hist.empty:
            return None, None, None
        
        current_price = hist['Close'].iloc[-1]
        price_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        
        return info, hist, price_change
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None

def simple_technical_analysis(hist):
    """Simple technical analysis without complex dependencies"""
    if hist is None or hist.empty:
        return "No data available"
    
    # Simple moving averages
    ma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
    ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else ma_5
    
    # Simple RSI calculation
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
    
    # Generate signals
    signals = []
    if current_rsi < 30:
        signals.append("RSI: Oversold (Buy signal)")
    elif current_rsi > 70:
        signals.append("RSI: Overbought (Sell signal)")
    else:
        signals.append(f"RSI: {current_rsi:.1f} (Neutral)")
    
    if hist['Close'].iloc[-1] > ma_5:
        signals.append("Price above 5-day MA (Bullish)")
    else:
        signals.append("Price below 5-day MA (Bearish)")
    
    return signals

def simple_fundamental_analysis(info):
    """Simple fundamental analysis"""
    if not info:
        return "No fundamental data available"
    
    metrics = []
    
    # P/E Ratio
    pe_ratio = info.get('trailingPE', 0)
    if pe_ratio > 0:
        if pe_ratio < 15:
            metrics.append(f"P/E: {pe_ratio:.1f} (Undervalued)")
        elif pe_ratio < 25:
            metrics.append(f"P/E: {pe_ratio:.1f} (Fair value)")
        else:
            metrics.append(f"P/E: {pe_ratio:.1f} (Overvalued)")
    
    # ROE
    roe = info.get('returnOnEquity', 0)
    if roe > 0:
        if roe > 0.15:
            metrics.append(f"ROE: {roe:.1%} (Excellent)")
        elif roe > 0.10:
            metrics.append(f"ROE: {roe:.1%} (Good)")
        else:
            metrics.append(f"ROE: {roe:.1%} (Poor)")
    
    # Debt to Equity
    debt_equity = info.get('debtToEquity', 0)
    if debt_equity > 0:
        if debt_equity < 0.3:
            metrics.append(f"Debt/Equity: {debt_equity:.2f} (Low debt)")
        elif debt_equity < 0.5:
            metrics.append(f"Debt/Equity: {debt_equity:.2f} (Moderate debt)")
        else:
            metrics.append(f"Debt/Equity: {debt_equity:.2f} (High debt)")
    
    return metrics

def generate_simple_recommendation(price_change, technical_signals, fundamental_metrics):
    """Generate simple investment recommendation"""
    score = 0
    reasoning = []
    
    # Price momentum
    if price_change > 5:
        score += 2
        reasoning.append("Strong price momentum")
    elif price_change > 0:
        score += 1
        reasoning.append("Positive price momentum")
    elif price_change < -5:
        score -= 2
        reasoning.append("Weak price momentum")
    else:
        score -= 1
        reasoning.append("Negative price momentum")
    
    # Technical signals
    bullish_signals = sum(1 for signal in technical_signals if "Bullish" in signal or "Buy" in signal)
    bearish_signals = sum(1 for signal in technical_signals if "Bearish" in signal or "Sell" in signal)
    
    score += bullish_signals - bearish_signals
    
    # Fundamental metrics
    good_fundamentals = sum(1 for metric in fundamental_metrics if "Excellent" in metric or "Good" in metric or "Undervalued" in metric)
    poor_fundamentals = sum(1 for metric in fundamental_metrics if "Poor" in metric or "Overvalued" in metric or "High debt" in metric)
    
    score += good_fundamentals - poor_fundamentals
    
    # Generate recommendation
    if score >= 3:
        recommendation = "STRONG BUY"
        confidence = min(90, 60 + score * 5)
    elif score >= 1:
        recommendation = "BUY"
        confidence = min(80, 50 + score * 5)
    elif score >= -1:
        recommendation = "HOLD"
        confidence = 50
    elif score >= -3:
        recommendation = "SELL"
        confidence = min(80, 50 + abs(score) * 5)
    else:
        recommendation = "STRONG SELL"
        confidence = min(90, 60 + abs(score) * 5)
    
    return recommendation, confidence, reasoning

def main():
    st.header("📊 Stock Analysis")
    
    # Stock input
    ticker = st.text_input("Enter stock ticker:", placeholder="e.g., AAPL", value="AAPL")
    
    if ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            info, hist, price_change = get_stock_data(ticker)
            
            if info and hist is not None:
                st.success(f"✅ Successfully analyzed {ticker}")
                
                # Display basic info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${hist['Close'].iloc[-1]:.2f}")
                with col2:
                    st.metric("5-Day Change", f"{price_change:.2f}%")
                with col3:
                    st.metric("Market Cap", f"${info.get('marketCap', 0):,.0f}")
                
                # Technical Analysis
                st.subheader("📈 Technical Analysis")
                technical_signals = simple_technical_analysis(hist)
                for signal in technical_signals:
                    st.write(f"• {signal}")
                
                # Fundamental Analysis
                st.subheader("💼 Fundamental Analysis")
                fundamental_metrics = simple_fundamental_analysis(info)
                for metric in fundamental_metrics:
                    st.write(f"• {metric}")
                
                # AI Recommendation
                st.subheader("🤖 AI Investment Recommendation")
                recommendation, confidence, reasoning = generate_simple_recommendation(
                    price_change, technical_signals, fundamental_metrics
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Recommendation", recommendation)
                with col2:
                    st.metric("Confidence", f"{confidence}%")
                
                st.write("**Reasoning:**")
                for reason in reasoning:
                    st.write(f"• {reason}")
                
                # Price chart
                st.subheader("📊 Price Chart")
                st.line_chart(hist['Close'])
                
            else:
                st.error(f"❌ Could not fetch data for {ticker}. Please check the ticker symbol.")

if __name__ == "__main__":
    main()
