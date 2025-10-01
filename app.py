import random
from datetime import datetime
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data_sources.news_articles import get_all_headlines
from data_sources.stock_prices import get_stock_summary, get_trending_stocks

from research_assistant.summarize_stock import (generate_stock_summary, suggest_stocks_to_watch,
                                                compare_risks_between_stocks)
from agent_reasoning.generate_hypotheses import generate_investment_hypothesis
from agent_reasoning.decision_maker import make_investment_decision
# , explain_why_trending

from utils.prompts import get_stock_summary_prompt
# from utils.email_sender import send_email_with_attachment
# from utils.pdf_report import generate_pdf_report
from utils.mood_tools import detect_macro_mood_label
from utils.mood_tracker import save_macro_mood
# from agent_reasoning.generate_hypotheses import generate_investment_hypothesis
# from agent_reasoning.decision_maker import make_investment_decision

from data_sources.earnings_reports import fetch_earnings_for_stock
from data_sources.stock_prices import get_cached_stock_summary
from portfolio.portfolio_allocator import fetch_current_prices, allocate_portfolio, allocate_portfolio_with_sector_preference, search_companies, get_popular_stocks, generate_weight_recommendations, get_market_insights, get_stock_sectors

# Cache functions for better performance
@st.cache_data(ttl=3600)  # Cache for 1 hour instead of default
def cached_search_companies(query: str, max_results: int = 10):
    return search_companies(query, max_results)

@st.cache_data(ttl=3600)  # Cache for 1 hour instead of default
def cached_get_popular_stocks():
    return get_popular_stocks()

# Pre-compute popular tickers set for faster validation
@st.cache_data(ttl=3600)
def get_popular_tickers_set():
    return {stock['ticker'].upper() for stock in get_popular_stocks()}

@st.cache_data(ttl=3600)  # cache result for 1 hour
def get_cached_stock_summary(ticker):
    return get_stock_summary(ticker)

# Process stock input function
def process_stock_input(input_text):
    if 'selected_stocks' not in st.session_state:
        st.session_state.selected_stocks = []
    
    items = [item.strip() for item in input_text.split(",") if item.strip()]
    added_stocks = []
    search_needed = []
    
    for item in items:
        item_upper = item.upper().strip()
        
        # Check if it's a valid ticker format
        if len(item_upper) <= 5 and item_upper.isalpha():
            # It looks like a ticker
            if item_upper not in st.session_state.selected_stocks:
                st.session_state.selected_stocks.append(item_upper)
                added_stocks.append(item_upper)
        else:
            # It might be a company name, add to search list
            search_needed.append(item)
    
    # Show results
    if added_stocks:
        st.success(f"✅ Added tickers: {', '.join(added_stocks)}")
    
    if search_needed:
        st.info(f"🔍 Need to search for: {', '.join(search_needed)}")
        
        # Search for company names
        for company_name in search_needed:
            search_results = cached_search_companies(company_name, 3)
            if search_results:
                st.markdown(f"**For '{company_name}':**")
                cols = st.columns(len(search_results))
                for i, company in enumerate(search_results):
                    with cols[i]:
                        if st.button(
                            f"{company['ticker']}\n{company['name'][:15]}...",
                            key=f"search_{company_name}_{company['ticker']}",
                            help=f"Add {company['ticker']}"
                        ):
                            if company['ticker'] not in st.session_state.selected_stocks:
                                st.session_state.selected_stocks.append(company['ticker'])
                                st.success(f"✅ Added {company['ticker']}")
                                st.rerun()
            else:
                st.warning(f"❌ No results found for '{company_name}'")

def generate_portfolio_pdf(allocation_data, budget, tech_preference):
    """
    Generate a PDF report for the portfolio allocation.
    """
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Portfolio Allocation Report', ln=True, align='C')
        pdf.ln(10)
        
        # Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Total Budget: ${budget:,.2f}', ln=True)
        pdf.cell(0, 10, f'Tech Preference: {tech_preference:.1%}', ln=True)
        pdf.ln(10)
        
        # Allocation table
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, 'Ticker', 1)
        pdf.cell(30, 10, 'Shares', 1)
        pdf.cell(40, 10, 'Amount', 1)
        pdf.cell(30, 10, 'Weight', 1)
        pdf.cell(30, 10, 'Price', 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 10)
        for row in allocation_data[:-1]:  # Exclude total row
            pdf.cell(40, 10, row['Ticker'], 1)
            pdf.cell(30, 10, row['Shares'], 1)
            pdf.cell(40, 10, row['Amount'], 1)
            pdf.cell(30, 10, row['Weight'], 1)
            pdf.cell(30, 10, row['Price'], 1)
            pdf.ln()
        
        # Save PDF
        filename = f"portfolio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        
        # Offer download
        with open(filename, "rb") as file:
            st.download_button(
                label="📄 Download PDF Report",
                data=file.read(),
                file_name=filename,
                mime="application/pdf"
            )
        
        # Clean up
        os.remove(filename)
        
    except Exception as e:
        st.error(f"❌ Failed to generate PDF: {e}")


def main():
st.set_page_config(page_title="AI Stock Advisor", page_icon="📈")

st.title("🤖 AI Stock Advisor")
st.markdown("Your LLM-powered assistant for investment research")
    
    # Add startup message
    st.success("🚀 **AI Stock Advisor is ready!** Enhanced with technical analysis, fundamental analysis, risk management, and backtesting capabilities.")

# ✅ Add spinner while fetching trending stocks
with st.spinner("Loading trending stocks..."):
    trending_stocks = get_trending_stocks(limit=30)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Stock Summary", "💡 Watchlist Suggestions", "📋 Compare Stocks", "💰 Portfolio Allocator", "🔬 Advanced Analysis"])

with tab1:
    st.header("📊 Get Market Summary for a Stock")
    st.markdown("### 🔥 Trending Stocks Options")

    n_trending = st.slider(
        "🔢 How many trending stocks to fetch?",
        min_value=5, max_value=30, value=10, step=1
    )

    trending = trending_stocks[:n_trending]
    trending_with_change = []

    for sym, name in trending:
        try:
            stock_info = get_cached_stock_summary(sym)

            # Handle errors gracefully
            if stock_info.get("error"):
                if "rate limit" in stock_info["error"].lower():
                    st.warning(f"⚠️ Rate limit hit while fetching {sym}. Try again shortly.")
                else:
                    st.error(f"❌ Could not fetch data for {sym}. Error: {stock_info['error']}")
                trending_with_change.append((sym, name, 0.0))
                continue

            hist = stock_info.get("history")
            if hist is not None and not hist.empty:
                price_change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100
                trending_with_change.append((sym, name, round(price_change, 2)))
            else:
                trending_with_change.append((sym, name, 0.0))

        except Exception as e:
            st.error(f"❌ Unexpected error while fetching {sym}: {e}")
            trending_with_change.append((sym, name, 0.0))

    tickers_display = [f"{sym} - {name} ({change:+.2f}%)" for sym, name, change in trending_with_change]

    selected_stocks = st.multiselect("📈 Pick one or more trending stocks to summarize", options=tickers_display)

    if st.button("🎲 Surprise Me with a Trending Stock") and tickers_display:
        random_stock = random.choice(tickers_display)
        st.success(f"🎯 Random pick: {random_stock}")
        selected_stocks = [random_stock]

    if selected_stocks:
        for selected_option in selected_stocks:
            ticker = selected_option.split(" - ")[0]
            st.markdown(f"### 📊 Summary for **{ticker}**")

            with st.spinner(f"Fetching data for {ticker}..."):
                stock_info = get_cached_stock_summary(ticker)

                # Handle API error messages early
                if stock_info.get("error"):
                    if "rate limit" in stock_info["error"].lower():
                        st.warning(f"⚠️ Rate limit hit while fetching {ticker}. Try again shortly.")
                    else:
                        st.error(f"❌ Could not fetch data for {ticker}. Error: {stock_info['error']}")
                    continue

                # Proceed with normal check
                hist = stock_info.get("history")
                if not stock_info.get("price") or hist is None or hist.empty:
                    st.error(f"❌ Could not fetch full data for {ticker}. Skipping.")
                    continue

                if hist is None or hist.empty:
                    st.warning(f"⚠️ No historical data for {ticker}. Displaying basic info only.")

                price_change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100

                # Price Chart
                st.markdown(f"### 📉 5-Day Price Trend for {ticker}")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode='lines+markers', name=f"{ticker} Price"))
                fig.update_layout(
                    title=f"{ticker} 5-Day Price Trend",
                    xaxis_title="Date", yaxis_title="Price ($)",
                    hovermode="x unified", xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)

                # Headlines and Summary
                headlines = get_all_headlines(ticker)
                mood_text, summary_text = generate_stock_summary(
                    ticker, stock_info["name"], stock_info["price"], price_change, headlines
                )

                mood_label = detect_macro_mood_label(mood_text)

                st.markdown("### 🧠 Macro Market Mood")
                if mood_label == "Risk-On":
                    st.success(mood_text)
                elif mood_label == "Risk-Off":
                    st.error(mood_text)
                else:
                    st.info(mood_text)

                save_macro_mood(mood_text)

                st.markdown(f"### 📋 Stock Summary")
                st.markdown(f"**Price:** ${stock_info['price']} &nbsp;&nbsp;&nbsp; **5-Day Change:** {price_change:.2f}%")

                earnings_data = fetch_earnings_for_stock(ticker)
                eps_surprise_value = earnings_data.get("eps_surprise", None)

                if isinstance(eps_surprise_value, (int, float)):
                    if eps_surprise_value > 0:
                        earnings_result = "Beat"
                        st.success(f"✅ EPS Surprise: {eps_surprise_value:+.2f}% (Beat)")
                    elif eps_surprise_value < 0:
                        earnings_result = "Miss"
                        st.error(f"❌ EPS Surprise: {eps_surprise_value:+.2f}% (Miss)")
                    else:
                        earnings_result = "Neutral"
                        st.info(f"ℹ️ EPS Surprise: {eps_surprise_value:+.2f}% (Neutral)")
                else:
                    earnings_result = "Neutral"

                st.markdown(summary_text)

                with st.spinner("💭 Generating investment hypothesis..."):
                    investment_hint = generate_investment_hypothesis(
                        macro_mood=mood_label,
                        earnings_result=earnings_result,
                        price_trend_percent=price_change
                    )

                st.markdown("### 💡 Investment Hypothesis")
                st.info(investment_hint)

                with st.spinner("🧠 Evaluating AI decision..."):
                    decision, confidence, explanation = make_investment_decision(
                        macro_mood=mood_label,
                        earnings_result=earnings_result,
                            price_change=price_change,
                            ticker=ticker,
                            include_technical=True,
                            include_fundamental=True,
                            include_risk=True,
                            include_backtest=True
                    )

                st.markdown("### 🤖 AI Investment Decision")
                st.success(f"**Decision: {decision}**  &nbsp;&nbsp;&nbsp; 🔍 **Confidence: {confidence}%**")
                st.markdown(explanation)

    else:
        st.info("Select or surprise-pick a stock to see the summary.")

    with tab5:
        st.header("🔬 Advanced Analysis")
        st.markdown("### 📈 Technical & Fundamental Analysis")
        
        # Stock selection for advanced analysis
        advanced_ticker = st.text_input("Enter stock ticker for advanced analysis:", placeholder="e.g., AAPL")
        
        if advanced_ticker:
            with st.spinner(f"Performing comprehensive analysis for {advanced_ticker}..."):
                try:
                    # Import analysis modules
                    from utils.technical_analysis import TechnicalAnalyzer
                    from utils.fundamental_analysis import FundamentalAnalyzer
                    from utils.risk_management import RiskManager
                    from utils.backtesting import Backtester
                    
                    # Initialize analyzers
                    technical_analyzer = TechnicalAnalyzer()
                    fundamental_analyzer = FundamentalAnalyzer()
                    risk_manager = RiskManager(portfolio_value=10000)
                    backtester = Backtester(initial_capital=10000)
                    
                    # Technical Analysis
                    st.markdown("#### 📈 Technical Analysis")
                    technical_signals = technical_analyzer.generate_technical_signals(advanced_ticker)
                    
                    if 'error' not in technical_signals:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Overall Signal", technical_signals.get('overall_signal', 'NEUTRAL'))
                        with col2:
                            st.metric("RSI", f"{technical_signals.get('rsi', 0):.1f}")
                        with col3:
                            st.metric("Confidence", f"{technical_signals.get('confidence', 0)}%")
                        
                        # Show detailed technical signals
                        st.markdown("**Detailed Technical Signals:**")
                        tech_data = []
                        tech_data.append({
                            "Indicator": "RSI",
                            "Value": f"{technical_signals.get('rsi', 0):.1f}",
                            "Signal": technical_signals.get('rsi_signal', {}).get('action', 'HOLD'),
                            "Strength": technical_signals.get('rsi_signal', {}).get('strength', 'NEUTRAL')
                        })
                        
                        # Add MA signals
                        for ma_signal in technical_signals.get('ma_signals', {}).get('signals', []):
                            tech_data.append({
                                "Indicator": ma_signal.get('type', 'MA'),
                                "Value": "N/A",
                                "Signal": ma_signal.get('signal', 'NEUTRAL'),
                                "Strength": "N/A"
                            })
                        
                        st.dataframe(pd.DataFrame(tech_data), use_container_width=True)
                    else:
                        st.error(f"Technical analysis error: {technical_signals.get('error', 'Unknown error')}")
                    
                    # Fundamental Analysis
                    st.markdown("#### 💼 Fundamental Analysis")
                    fundamental_analysis = fundamental_analyzer.analyze_fundamentals(advanced_ticker)
                    
                    if 'error' not in fundamental_analysis:
                        fundamental_score = fundamental_analysis.get('fundamental_score', {})
                        recommendation = fundamental_analysis.get('recommendation', {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fundamental Score", f"{fundamental_score.get('score_percentage', 0):.1f}%")
                        with col2:
                            st.metric("Rating", fundamental_score.get('rating', 'N/A'))
                        with col3:
                            st.metric("Recommendation", recommendation.get('recommendation', 'N/A'))
                        
                        # Show valuation metrics
                        valuation_metrics = fundamental_analysis.get('valuation_metrics', {})
                        st.markdown("**Valuation Metrics:**")
                        val_data = []
                        val_data.append({
                            "Metric": "P/E Ratio",
                            "Value": f"{valuation_metrics.get('pe_ratio', 0):.2f}"
                        })
                        val_data.append({
                            "Metric": "Price to Book",
                            "Value": f"{valuation_metrics.get('price_to_book', 0):.2f}"
                        })
                        val_data.append({
                            "Metric": "Dividend Yield",
                            "Value": f"{valuation_metrics.get('dividend_yield', 0):.2%}"
                        })
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.dataframe(pd.DataFrame(val_data), use_container_width=True)
                        
                        # Show financial ratios
                        financial_ratios = fundamental_analysis.get('financial_ratios', {})
                        st.markdown("**Financial Ratios:**")
                        ratio_data = []
                        ratio_data.append({
                            "Ratio": "ROE",
                            "Value": f"{financial_ratios.get('roe', 0):.2%}"
                        })
                        ratio_data.append({
                            "Ratio": "ROA",
                            "Value": f"{financial_ratios.get('roa', 0):.2%}"
                        })
                        ratio_data.append({
                            "Ratio": "Debt/Equity",
                            "Value": f"{financial_ratios.get('debt_to_equity', 0):.2f}"
                        })
                        
                        with col2:
                            st.dataframe(pd.DataFrame(ratio_data), use_container_width=True)
                    else:
                        st.error(f"Fundamental analysis error: {fundamental_analysis.get('error', 'Unknown error')}")
                    
                    # Backtesting
                    st.markdown("#### 📈 Strategy Backtesting")
                    strategy_params = {
                        'rsi_period': 14,
                        'rsi_oversold': 30,
                        'rsi_overbought': 70,
                        'ma_short': 20,
                        'ma_long': 50,
                        'stop_loss': 0.05,
                        'take_profit': 0.10
                    }
                    
                    backtest_results = backtester.backtest_strategy(advanced_ticker, strategy_params)
                    
                    if 'error' not in backtest_results:
                        performance_metrics = backtest_results.get('performance_metrics', {})
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Return", f"{performance_metrics.get('total_return', 0):.2%}")
                        with col2:
                            st.metric("Sharpe Ratio", f"{performance_metrics.get('sharpe_ratio', 0):.2f}")
                        with col3:
                            st.metric("Max Drawdown", f"{performance_metrics.get('max_drawdown', 0):.2%}")
                        with col4:
                            st.metric("Win Rate", f"{performance_metrics.get('win_rate', 0):.2%}")
                        
                        # Show performance report
                        st.markdown("**Performance Report:**")
                        st.markdown(backtester.generate_performance_report(backtest_results))
                    else:
                        st.error(f"Backtesting error: {backtest_results.get('error', 'Unknown error')}")
                    
                except Exception as e:
                    st.error(f"Error during advanced analysis: {e}")
                    st.info("💡 **Troubleshooting Tips:**")
                    st.markdown("""
                    - Make sure the ticker symbol is correct (e.g., AAPL, MSFT, TSLA)
                    - Check your internet connection for data fetching
                    - Try refreshing the page if the error persists
                    - Some analysis features may take a few moments to load
                    """)
    
with tab2:
    st.header("💡 Get Investment Suggestions")

    if st.button("Suggest Top Stocks to Watch"):
        with st.spinner("Fetching trending tickers and analyzing..."):
            # 1. Fetch 10 trending stocks
            trending = trending_stocks[:10]

            # 2. Display all 10 trending stocks
            df = pd.DataFrame(trending, columns=["Ticker", "Company"])
            st.markdown("### 🔥 Currently Trending Tickers")
            st.dataframe(df, hide_index=True)

            # 3. Let user choose: Top 3 vs All 10
            choice = st.radio(
                "📈 How many stocks would you like to get analysis on?",
                options=["Top 3 only", "All 10"],
                index=0
            )

            if choice == "Top 3 only":
                selected = trending[:3]

                trending_formatted = "\n".join([f"- {ticker} ({name})" for ticker, name in selected])
                prompt = f"""
            You are a stock market investment assistant.

            Here are the trending stocks:
            {trending_formatted}

            For each stock above, briefly explain whether it's a good opportunity to watch or invest in now. 
            Write 1–2 sentences for each. 
            Respond in a clean readable bullet point format.
            """
                suggestions = suggest_stocks_to_watch(ticker_list=selected, custom_prompt=prompt)

            else:
                selected = trending[:10]  # go back to full 10
                suggestions = suggest_stocks_to_watch(ticker_list=selected)  # NO custom_prompt for batching to work

            # 5. Call GPT to generate suggestions
            st.write(f"🧪 Sending {len(selected)} tickers to suggest_stocks_to_watch")

            # Debugging GPT output
            if choice == "Top 3 only":
                st.markdown("### 🔍 Prompt Preview")
                st.code(prompt)

            if not suggestions:
                st.error("⚠️ GPT returned an empty response.")
            else:
                st.markdown("### 🧠 GPT Watchlist Suggestions")
                st.markdown(suggestions)

with tab3:
    st.header("📋 Compare Multiple Stocks Side by Side")

    trending = trending_stocks[:10]
    ticker_choices = [f"{sym} - {name}" for sym, name in trending]

    selected_tickers = st.multiselect(
        "Pick 2 or 3 stocks to compare:",
        options=ticker_choices,
        default=ticker_choices[:2],
        max_selections=3
    )

    tickers_only = [s.split(" - ")[0] for s in selected_tickers]

    if len(tickers_only) >= 2:
        cols = st.columns(len(tickers_only))
        summaries = []
        all_headlines = []

        for idx, ticker in enumerate(tickers_only):
            with cols[idx]:
                st.subheader(f"📈 {ticker}")
                stock_info = get_cached_stock_summary(ticker)
                headlines = get_all_headlines(ticker)
                all_headlines.append((ticker, headlines))

                hist = stock_info.get("history")
                if hist is None or hist.empty:
                    st.error(f"⚠️ No data for {ticker}")
                    continue

                price_change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100

                summary = generate_stock_summary(
                    ticker,
                    stock_info["name"],
                    stock_info["price"],
                    price_change,
                    headlines
                )
                summaries.append((ticker, summary))
                st.markdown(summary)

        # Add GPT risk comparison section
        if len(tickers_only) >= 2:
            # Email + PDF export
            st.markdown("### 📩 Email Report")
            email = st.text_input("Enter your email to receive this as a PDF report")
                # PDF and email features temporarily disabled for cloud deployment
                st.info("📧 **PDF Report & Email features are temporarily disabled for cloud deployment**")
                st.markdown("""
                **Alternative options:**
                - Copy the analysis text above
                - Take screenshots of the charts
                - Use the data tables for your records
                """)
    
    with tab4:
        st.header("💰 Portfolio Allocator")
        st.markdown("Suggest how to allocate your budget across selected stocks with sector preferences.")
        
        budget = st.number_input("Enter your total budget ($)", min_value=100.0, value=1000.0, step=10.0)
        
        # Tech preference slider
        tech_preference = st.slider(
            "🎯 Tech Stock Preference", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.6, 
            step=0.05,
            help="Percentage of budget to allocate to technology stocks. 0.0 = no tech preference, 1.0 = only tech stocks."
        )
        
        # Toggle between trending and custom stocks
        stock_source = st.radio(
            "📈 Stock Selection Method",
            options=["🔥 Use Trending Stocks", "✏️ Enter Custom Stocks"],
            index=1,  # Default to custom stocks (index 1)
            help="Choose between trending stocks from Yahoo Finance or enter your own stock list"
        )
        
        selected_symbols = []
        
        if stock_source == "🔥 Use Trending Stocks":
            # Original trending stocks functionality
            trending = trending_stocks  # list of (symbol, name)
            trending_symbols = [sym for sym, name in trending]
            trending_display = [f"{sym} - {name}" for sym, name in trending]
            selected_display = st.multiselect("Select stocks to allocate", trending_display)
            selected_symbols = [s.split(" - ")[0] for s in selected_display]
            
        else:
            # Manual stock entry
            st.markdown("#### ✏️ Enter Your Stock List")
            
            # Add tabs for different input methods
            input_tab1, input_tab2 = st.tabs(["🎯 Smart Input", "⭐ Popular Stocks"])
            
            # Initialize session state
            if 'selected_stocks' not in st.session_state:
                st.session_state.selected_stocks = []
            if 'search_results' not in st.session_state:
                st.session_state.search_results = {}
            if 'pending_additions' not in st.session_state:
                st.session_state.pending_additions = []
            
            # Process any pending additions (optimization to reduce reruns)
            if st.session_state.pending_additions:
                st.session_state.selected_stocks.extend(st.session_state.pending_additions)
                st.success(f"✅ Added {len(st.session_state.pending_additions)} stocks: {', '.join(st.session_state.pending_additions)}")
                st.session_state.pending_additions = []
                st.session_state.search_results = {}
            
            with input_tab1:
                st.markdown("**Add multiple stocks at once:**")
                st.markdown("Type tickers directly (AAPL, MSFT) or company names (Apple, Target) - separate with commas")
                
                # Show currently selected stocks
                if st.session_state.selected_stocks:
                    st.markdown("**📊 Selected Stocks:**")
                    for i, stock in enumerate(st.session_state.selected_stocks):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"• {stock}")
                        with col2:
                            if st.button("Remove", key=f"remove_{i}"):
                                st.session_state.selected_stocks.pop(i)
                                st.rerun()
                
                # Use form to handle Enter key
                with st.form("add_stocks_form"):
                    user_input = st.text_input(
                        "Add stocks",
                        placeholder="AAPL, MSFT, Apple, Target, GOOGL",
                        help="Type tickers or company names separated by commas, then press Enter or click Add",
                        key="multi_input"
                    )
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        submitted = st.form_submit_button("Add Stocks")
                    with col2:
                        if st.form_submit_button("Clear All"):
                            st.session_state.selected_stocks = []
                            st.session_state.search_results = {}
                            st.rerun()
                    
                    # Process input when form is submitted (Enter key or button click)
                    if submitted and user_input:
                        # Process the input directly (optimized)
                        items = [item.strip() for item in user_input.split(",") if item.strip()]
                        added_stocks = []
                        search_needed = []
                        
                        # Get popular stocks once for validation
                        popular_tickers = get_popular_tickers_set()
                        
                        for item in items:
                            item_upper = item.upper().strip()
                            
                            # Check if it's a valid ticker (optimized validation)
                            if (len(item_upper) <= 5 and 
                                item_upper.isalpha() and 
                                item_upper in popular_tickers):
                                # Valid ticker
                                if item_upper not in st.session_state.selected_stocks:
                                    st.session_state.selected_stocks.append(item_upper)
                                    added_stocks.append(item_upper)
                            else:
                                # Company name for search
                                search_needed.append(item)
                        
                        # Show results
                        if added_stocks:
                            st.success(f"✅ Added tickers: {', '.join(added_stocks)}")
                        
                        if search_needed:
                            st.info(f"🔍 Need to search for: {', '.join(search_needed)}")
                            
                            # Search for company names and store results in session state
                            for company_name in search_needed:
                                search_results = cached_search_companies(company_name, 3)
                                st.session_state.search_results[company_name] = search_results
            
            # Display search results outside the form (so buttons work)
            if st.session_state.search_results:
                st.markdown("**🔍 Search Results - Select Multiple Stocks:**")
                
                # Collect all search results into one list (optimized)
                all_search_results = []
                for company_name, search_results in st.session_state.search_results.items():
                    if search_results:
                        all_search_results.extend(search_results)
                    else:
                        st.warning(f"❌ No results found for '{company_name}'")
                
                # Remove duplicates and create options for multi-select (optimized)
                unique_results = []
                seen_tickers = set()
                options = []
                
                for result in all_search_results:
                    ticker = result['ticker']
                    if ticker not in seen_tickers:
                        unique_results.append(result)
                        seen_tickers.add(ticker)
                        options.append(f"{ticker} - {result['name']}")
                
                if options:
                    # Simple text input approach - no auto-rerun issues
                    st.markdown("**📋 Available stocks from your search:**")
                    
                    # Show available options
                    st.markdown("**Available stocks:**")
                    for option in options:
                        st.write(f"• {option}")
                    
                    st.markdown("---")
                    st.markdown("**🎯 Add stocks by typing their tickers:**")
                    
                    # Simple text input for tickers
                    ticker_input = st.text_input(
                        "Type tickers to add (separated by commas):",
                        placeholder="TGT, AMZN, AAPL",
                        help="Type the tickers you want to add, separated by commas"
                    )
                    
                    # Add button - only processes when clicked
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button("➕ Add These Stocks", key="add_from_text"):
                            if ticker_input.strip():
                                # Process the ticker input
                                input_tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
                                valid_tickers = []
                                invalid_tickers = []
                                
                                # Validate against available options
                                available_tickers = {option.split(" - ")[0] for option in options}
                                
                                for ticker in input_tickers:
                                    if ticker in available_tickers:
                                        if ticker not in st.session_state.selected_stocks:
                                            valid_tickers.append(ticker)
                                        else:
                                            st.warning(f"⚠️ {ticker} is already in your list")
                                    else:
                                        invalid_tickers.append(ticker)
                                
                                # Add valid tickers
                                if valid_tickers:
                                    st.session_state.pending_additions = valid_tickers
                                    st.success(f"✅ Will add: {', '.join(valid_tickers)}")
                                    st.rerun()
                                
                                # Show invalid tickers
                                if invalid_tickers:
                                    st.error(f"❌ Invalid tickers: {', '.join(invalid_tickers)}")
                                    st.info("Please use only tickers from the available list above")
                    
                    with col2:
                        if st.button("🗑️ Clear Search Results", key="clear_search_results"):
                            st.session_state.search_results = {}
                            st.rerun()
            
            # Use selected stocks from session state
            selected_symbols = st.session_state.selected_stocks.copy()
            
            with input_tab2:
                st.markdown("**Quick select from popular stocks:**")
                
                popular_stocks = cached_get_popular_stocks()
                
                # Group by sector for better organization
                sectors = {}
                for stock in popular_stocks:
                    sector = stock['sector']
                    if sector not in sectors:
                        sectors[sector] = []
                    sectors[sector].append(stock)
                
                # Track changes to avoid unnecessary reruns
                if 'popular_selections' not in st.session_state:
                    st.session_state.popular_selections = set()
                
                selected_from_popular = []
                
                for sector, stocks in sectors.items():
                    st.markdown(f"**{sector}:**")
                    cols = st.columns(3)
                    for i, stock in enumerate(stocks):
                        col_idx = i % 3
                        with cols[col_idx]:
                            display_text = f"{stock['name']} ({stock['ticker']})"
                            checkbox_key = f"popular_{stock['ticker']}"
                            
                            # Check if this stock was previously selected
                            is_selected = stock['ticker'] in st.session_state.popular_selections
                            
                            if st.checkbox(display_text, value=is_selected, key=checkbox_key):
                                selected_from_popular.append(stock['ticker'])
                                st.session_state.popular_selections.add(stock['ticker'])
                            elif is_selected:
                                # Remove from selections if unchecked
                                st.session_state.popular_selections.discard(stock['ticker'])
                
                # Only update if there are changes
                if selected_from_popular:
                    # Add to session state
                    if 'selected_stocks' not in st.session_state:
                        st.session_state.selected_stocks = []
                    
                    added_count = 0
                    for ticker in selected_from_popular:
                        if ticker not in st.session_state.selected_stocks:
                            st.session_state.selected_stocks.append(ticker)
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"✅ Added {added_count} new stocks")
                        st.rerun()
            
            # Show final selected stocks summary
            if selected_symbols:
                st.markdown(f"**📊 Final Selected Stocks ({len(selected_symbols)}):** {', '.join(selected_symbols)}")
        
        # Portfolio Allocation
        if selected_symbols and budget > 0:
            st.markdown("---")
            st.markdown("## 📊 Portfolio Allocation")
            
            # Fetch current prices
            with st.spinner("Fetching current stock prices..."):
                prices = fetch_current_prices(selected_symbols)
            
            if prices:
                # Display current prices
                st.markdown("### 💰 Current Prices")
                price_data = []
                for ticker in selected_symbols:
                    price = prices.get(ticker)
                    if price:
                        price_data.append({"Ticker": ticker, "Current Price": f"${price:.2f}"})
                
                if price_data:
                    st.dataframe(pd.DataFrame(price_data), use_container_width=True)
                
                # Market Insights and Weight Recommendations
                st.markdown("### 🧠 AI Weight Recommendations")
                
                # Get market insights
                with st.spinner("Analyzing market conditions..."):
                    insights = get_market_insights(selected_symbols)
                    recommended_weights = generate_weight_recommendations(selected_symbols, tech_preference)
                
                # Display insights
                st.markdown("**📈 Market Analysis:**")
                insight_data = []
                for ticker in selected_symbols:
                    insight_data.append({
                        "Ticker": ticker,
                        "Market Insights": insights.get(ticker, "📊 Data unavailable")
                    })
                
                st.dataframe(pd.DataFrame(insight_data), use_container_width=True)
                
                # Weight recommendation section
                st.markdown("### ⚖️ Portfolio Weights")
                
                # Toggle between AI recommendations and manual weights
                weight_method = st.radio(
                    "Choose weight method:",
                    options=["🤖 Use AI Recommendations", "✏️ Manual Weights"],
                    help="AI recommendations consider market conditions, sector analysis, and your tech preference"
                )
                
                if weight_method == "🤖 Use AI Recommendations":
                    st.markdown("**🎯 AI Recommended Weights:**")
                    
                    # Display recommended weights
                    weight_data = []
                    for ticker in selected_symbols:
                        weight = recommended_weights.get(ticker, 0)
                        weight_data.append({
                            "Ticker": ticker,
                            "Recommended Weight": f"{weight:.1%}",
                            "Reasoning": insights.get(ticker, "📊 Standard allocation")
                        })
                    
                    st.dataframe(pd.DataFrame(weight_data), use_container_width=True)
                    
                    # Use recommended weights for allocation
                    custom_weights = recommended_weights
                    
                    st.success("✅ Using AI-recommended weights based on market analysis!")
                    
                else:  # Manual weights
                    st.markdown("**✏️ Set Manual Weights:**")
                    st.markdown("Adjust the weights below (must sum to 100%):")
                    
                    # Manual weight inputs
                    manual_weights = {}
                    total_weight = 0
                    
                    col1, col2 = st.columns(2)
                    for i, ticker in enumerate(selected_symbols):
                        with col1 if i % 2 == 0 else col2:
                            weight = st.slider(
                                f"{ticker} Weight (%)",
                                min_value=0,
                                max_value=100,
                                value=int(100 / len(selected_symbols)),  # Equal weight default
                                key=f"weight_{ticker}"
                            )
                            manual_weights[ticker] = weight / 100
                            total_weight += weight
                    
                    # Show total weight
                    if total_weight != 100:
                        st.warning(f"⚠️ Total weight: {total_weight}% (should be 100%)")
                    else:
                        st.success("✅ Total weight: 100% - Ready for allocation!")
                    
                    custom_weights = manual_weights if total_weight == 100 else None
                
                # Allocate portfolio
                if custom_weights:
                    st.markdown("### 📋 Allocation Results")
                    
                    # Debug: Show the weights being used
                    st.markdown("**🔍 Debug - Weights being used:**")
                    for ticker, weight in custom_weights.items():
                        st.write(f"{ticker}: {weight:.1%}")
                    
                    with st.spinner("Calculating optimal allocation..."):
                        allocation = allocate_portfolio_with_sector_preference(
                            budget=budget,
                            tickers=selected_symbols,
                            prices=prices,
                            tech_preference=tech_preference,
                            custom_weights=custom_weights
                        )
                    
                    if allocation:
                        # Display allocation results
                        allocation_data = []
                        total_invested = 0
                        unused_budget = budget
                        
                        # Debug: Show raw allocation data
                        st.markdown("**🔍 Debug - Raw allocation data:**")
                        for item in allocation:
                            st.write(f"{item['ticker']}: Weight={item['weight']:.1%}, Shares={item['shares']}, Price=${item['price']:.2f}, Allocated=${item['allocated']:.2f}")
                        
                        for item in allocation:
                            ticker = item['ticker']
                            shares = item['shares']
                            allocated = item['allocated']
                            weight = item['weight']
                            price = prices.get(ticker, 0)
                            total_invested += allocated
                            unused_budget -= allocated
                            
                            # Show fractional alternative if no shares bought
                            if shares == 0 and item.get('fractional_shares', 0) > 0:
                                fractional_shares = item['fractional_shares']
                                fractional_allocated = item['fractional_allocated']
                                allocation_data.append({
                                    "Ticker": ticker,
                                    "Shares (Whole)": f"{shares:.0f}",
                                    "Shares (Fractional)": f"{fractional_shares:.2f}",
                                    "Amount (Whole)": f"${allocated:,.2f}",
                                    "Amount (Fractional)": f"${fractional_allocated:,.2f}",
                                    "Weight": f"{weight:.1%}",
                                    "Price": f"${price:.2f}"
                                })
                            else:
                                allocation_data.append({
                                    "Ticker": ticker,
                                    "Shares (Whole)": f"{shares:.0f}",
                                    "Shares (Fractional)": f"{shares:.0f}",
                                    "Amount (Whole)": f"${allocated:,.2f}",
                                    "Amount (Fractional)": f"${allocated:,.2f}",
                                    "Weight": f"{weight:.1%}",
                                    "Price": f"${price:.2f}"
                                })
                        
                        # Add total row
                        allocation_data.append({
                            "Ticker": "**TOTAL**",
                            "Shares (Whole)": "",
                            "Shares (Fractional)": "",
                            "Amount (Whole)": f"**${total_invested:,.2f}**",
                            "Amount (Fractional)": f"**${budget:,.2f}**",
                            "Weight": "**100%**",
                            "Price": ""
                        })
                        
                        st.dataframe(pd.DataFrame(allocation_data), use_container_width=True)
                        
                        # Show budget analysis
                        st.markdown("### 💰 Budget Analysis")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Budget", f"${budget:,.2f}")
                        with col2:
                            st.metric("Allocated (Whole Shares)", f"${total_invested:,.2f}")
                        with col3:
                            st.metric("Unused Budget", f"${unused_budget:,.2f}")
                        
                        # Provide recommendations
                        if unused_budget > budget * 0.1:  # If more than 10% unused
                            st.warning(f"⚠️ **High unused budget (${unused_budget:,.2f})** - Consider:")
                            st.markdown("""
                            **Options to use your full budget:**
                            - **Fractional shares**: Many brokers support fractional share trading
                            - **Adjust weights**: Give more weight to cheaper stocks
                            - **Add more stocks**: Include lower-priced stocks
                            - **Increase budget**: Consider a larger investment amount
                            """)
                        else:
                            st.success("✅ **Good budget utilization** - Most of your budget is allocated!")
                        
                        # Export options
                        st.markdown("### 📤 Export Options")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # CSV export
                            csv_data = pd.DataFrame(allocation_data[:-1])  # Exclude total row
                            csv = csv_data.to_csv(index=False)
                            st.download_button(
                                label="📄 Download CSV",
                                data=csv,
                                file_name=f"portfolio_allocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        
                        with col2:
                            # PDF export
                            if st.button("📋 Generate PDF Report"):
                                with st.spinner("Generating PDF report..."):
                                    generate_portfolio_pdf(allocation_data, budget, tech_preference)
                                st.success("✅ PDF report generated!")
                    else:
                        st.error("❌ Failed to calculate allocation. Please check your inputs.")
            else:
                st.error("❌ Failed to fetch current prices. Please check your stock symbols.")
                else:
            if not selected_symbols:
                st.info("ℹ️ Please select some stocks to allocate.")
            if budget <= 0:
                st.info("ℹ️ Please enter a budget greater than $0.")


# Main app
if __name__ == "__main__":
    main()