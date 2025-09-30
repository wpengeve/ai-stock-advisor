import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Optional
import requests
from datetime import datetime

class FundamentalAnalyzer:
    """
    Enhanced fundamental analysis module for comprehensive stock evaluation.
    """
    
    def __init__(self):
        self.valuation_metrics = {}
        self.financial_ratios = {}
    
    def analyze_fundamentals(self, ticker: str) -> Dict[str, any]:
        """
        Perform comprehensive fundamental analysis.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dict with fundamental analysis results
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Basic company info
            company_info = {
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0)
            }
            
            # Valuation metrics
            valuation = self._calculate_valuation_metrics(info)
            
            # Financial ratios
            ratios = self._calculate_financial_ratios(info)
            
            # Cash flow analysis
            cash_flow = self._analyze_cash_flow(stock)
            
            # Debt analysis
            debt_analysis = self._analyze_debt(info)
            
            # Growth metrics
            growth_metrics = self._calculate_growth_metrics(stock)
            
            # Quality metrics
            quality_metrics = self._calculate_quality_metrics(info)
            
            # Overall scoring
            fundamental_score = self._calculate_fundamental_score(
                valuation, ratios, cash_flow, debt_analysis, growth_metrics, quality_metrics
            )
            
            return {
                'ticker': ticker,
                'company_info': company_info,
                'valuation_metrics': valuation,
                'financial_ratios': ratios,
                'cash_flow_analysis': cash_flow,
                'debt_analysis': debt_analysis,
                'growth_metrics': growth_metrics,
                'quality_metrics': quality_metrics,
                'fundamental_score': fundamental_score,
                'recommendation': self._generate_fundamental_recommendation(fundamental_score)
            }
            
        except Exception as e:
            return {"error": f"Error analyzing fundamentals for {ticker}: {e}"}
    
    def _calculate_valuation_metrics(self, info: Dict) -> Dict[str, float]:
        """Calculate valuation metrics."""
        return {
            'pe_ratio': info.get('trailingPE', 0),
            'forward_pe': info.get('forwardPE', 0),
            'price_to_book': info.get('priceToBook', 0),
            'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
            'ev_to_ebitda': info.get('enterpriseToEbitda', 0),
            'price_to_cash_flow': info.get('priceToCashflowTrailing12Months', 0),
            'dividend_yield': info.get('dividendYield', 0) or 0,
            'payout_ratio': info.get('payoutRatio', 0)
        }
    
    def _calculate_financial_ratios(self, info: Dict) -> Dict[str, float]:
        """Calculate key financial ratios."""
        return {
            'roe': info.get('returnOnEquity', 0),
            'roa': info.get('returnOnAssets', 0),
            'roic': info.get('returnOnInvestedCapital', 0),
            'gross_margin': info.get('grossMargins', 0),
            'operating_margin': info.get('operatingMargins', 0),
            'net_margin': info.get('netIncomeToCommon', 0),
            'current_ratio': info.get('currentRatio', 0),
            'quick_ratio': info.get('quickRatio', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'interest_coverage': info.get('interestCoverage', 0)
        }
    
    def _analyze_cash_flow(self, stock: yf.Ticker) -> Dict[str, any]:
        """Analyze cash flow metrics."""
        try:
            # Get cash flow data
            cash_flow = stock.cashflow
            if cash_flow is None or cash_flow.empty:
                return {"error": "No cash flow data available"}
            
            # Calculate key cash flow metrics
            operating_cf = cash_flow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cash_flow.index else 0
            investing_cf = cash_flow.loc['Investing Cash Flow'].iloc[0] if 'Investing Cash Flow' in cash_flow.index else 0
            financing_cf = cash_flow.loc['Financing Cash Flow'].iloc[0] if 'Financing Cash Flow' in cash_flow.index else 0
            
            # Free cash flow calculation
            capex = cash_flow.loc['Capital Expenditure'].iloc[0] if 'Capital Expenditure' in cash_flow.index else 0
            free_cash_flow = operating_cf + capex  # Capex is typically negative
            
            return {
                'operating_cash_flow': operating_cf,
                'investing_cash_flow': investing_cf,
                'financing_cash_flow': financing_cf,
                'free_cash_flow': free_cash_flow,
                'capex': capex,
                'cash_flow_quality': 'GOOD' if operating_cf > 0 else 'POOR'
            }
            
        except Exception as e:
            return {"error": f"Error analyzing cash flow: {e}"}
    
    def _analyze_debt(self, info: Dict) -> Dict[str, any]:
        """Analyze debt levels and structure."""
        total_debt = info.get('totalDebt', 0)
        total_cash = info.get('totalCash', 0)
        net_debt = total_debt - total_cash
        
        debt_to_equity = info.get('debtToEquity', 0)
        interest_coverage = info.get('interestCoverage', 0)
        
        # Debt rating
        debt_rating = 'LOW'
        if debt_to_equity > 0.5:
            debt_rating = 'HIGH'
        elif debt_to_equity > 0.3:
            debt_rating = 'MEDIUM'
        
        return {
            'total_debt': total_debt,
            'total_cash': total_cash,
            'net_debt': net_debt,
            'debt_to_equity': debt_to_equity,
            'interest_coverage': interest_coverage,
            'debt_rating': debt_rating
        }
    
    def _calculate_growth_metrics(self, stock: yf.Ticker) -> Dict[str, float]:
        """Calculate growth metrics."""
        try:
            # Get earnings data
            earnings = stock.earnings
            if earnings is None or earnings.empty:
                return {"error": "No earnings data available"}
            
            # Calculate growth rates
            if len(earnings) >= 2:
                revenue_growth = ((earnings['Revenue'].iloc[-1] - earnings['Revenue'].iloc[-2]) / 
                                earnings['Revenue'].iloc[-2]) if 'Revenue' in earnings.columns else 0
                eps_growth = ((earnings['Earnings'].iloc[-1] - earnings['Earnings'].iloc[-2]) / 
                             earnings['Earnings'].iloc[-2]) if 'Earnings' in earnings.columns else 0
            else:
                revenue_growth = 0
                eps_growth = 0
            
            return {
                'revenue_growth': revenue_growth,
                'eps_growth': eps_growth,
                'growth_rating': 'HIGH' if revenue_growth > 0.15 else 'MEDIUM' if revenue_growth > 0.05 else 'LOW'
            }
            
        except Exception as e:
            return {"error": f"Error calculating growth metrics: {e}"}
    
    def _calculate_quality_metrics(self, info: Dict) -> Dict[str, any]:
        """Calculate quality metrics."""
        roe = info.get('returnOnEquity', 0)
        roa = info.get('returnOnAssets', 0)
        gross_margin = info.get('grossMargins', 0)
        operating_margin = info.get('operatingMargins', 0)
        
        # Quality score based on profitability
        quality_score = 0
        if roe > 0.15:
            quality_score += 25
        elif roe > 0.10:
            quality_score += 15
        elif roe > 0.05:
            quality_score += 5
        
        if roa > 0.10:
            quality_score += 25
        elif roa > 0.05:
            quality_score += 15
        elif roa > 0.02:
            quality_score += 5
        
        if gross_margin > 0.40:
            quality_score += 25
        elif gross_margin > 0.20:
            quality_score += 15
        elif gross_margin > 0.10:
            quality_score += 5
        
        if operating_margin > 0.20:
            quality_score += 25
        elif operating_margin > 0.10:
            quality_score += 15
        elif operating_margin > 0.05:
            quality_score += 5
        
        quality_rating = 'HIGH' if quality_score >= 75 else 'MEDIUM' if quality_score >= 50 else 'LOW'
        
        return {
            'quality_score': quality_score,
            'quality_rating': quality_rating,
            'roe': roe,
            'roa': roa,
            'gross_margin': gross_margin,
            'operating_margin': operating_margin
        }
    
    def _calculate_fundamental_score(self, valuation: Dict, ratios: Dict, 
                                   cash_flow: Dict, debt: Dict, growth: Dict, quality: Dict) -> Dict[str, any]:
        """Calculate overall fundamental score."""
        score = 0
        max_score = 100
        
        # Valuation score (25 points)
        pe_ratio = valuation.get('pe_ratio', 0)
        if 0 < pe_ratio < 15:
            score += 25
        elif 0 < pe_ratio < 25:
            score += 15
        elif 0 < pe_ratio < 35:
            score += 5
        
        # Financial health score (25 points)
        debt_to_equity = debt.get('debt_to_equity', 0)
        if debt_to_equity < 0.3:
            score += 25
        elif debt_to_equity < 0.5:
            score += 15
        elif debt_to_equity < 0.7:
            score += 5
        
        # Profitability score (25 points)
        roe = ratios.get('roe', 0)
        if roe > 0.15:
            score += 25
        elif roe > 0.10:
            score += 15
        elif roe > 0.05:
            score += 5
        
        # Growth score (25 points)
        revenue_growth = growth.get('revenue_growth', 0)
        if revenue_growth > 0.15:
            score += 25
        elif revenue_growth > 0.10:
            score += 15
        elif revenue_growth > 0.05:
            score += 5
        
        # Calculate percentage
        score_percentage = (score / max_score) * 100
        
        # Determine rating
        if score_percentage >= 80:
            rating = 'EXCELLENT'
        elif score_percentage >= 60:
            rating = 'GOOD'
        elif score_percentage >= 40:
            rating = 'FAIR'
        else:
            rating = 'POOR'
        
        return {
            'score': score,
            'score_percentage': score_percentage,
            'rating': rating,
            'max_score': max_score
        }
    
    def _generate_fundamental_recommendation(self, fundamental_score: Dict) -> Dict[str, str]:
        """Generate investment recommendation based on fundamental score."""
        score_pct = fundamental_score.get('score_percentage', 0)
        rating = fundamental_score.get('rating', 'POOR')
        
        if rating == 'EXCELLENT':
            recommendation = 'STRONG_BUY'
            reasoning = 'Excellent fundamentals with strong profitability, low debt, and good growth prospects.'
        elif rating == 'GOOD':
            recommendation = 'BUY'
            reasoning = 'Good fundamentals with solid financial health and reasonable valuation.'
        elif rating == 'FAIR':
            recommendation = 'HOLD'
            reasoning = 'Fair fundamentals with some concerns. Monitor for improvement.'
        else:
            recommendation = 'SELL'
            reasoning = 'Poor fundamentals with significant concerns about financial health or valuation.'
        
        return {
            'recommendation': recommendation,
            'reasoning': reasoning,
            'confidence': min(90, score_pct + 10)
        }
    
    def compare_fundamentals(self, tickers: List[str]) -> Dict[str, any]:
        """
        Compare fundamental metrics across multiple stocks.
        
        Args:
            tickers: List of stock tickers
        
        Returns:
            Dict with comparison results
        """
        results = {}
        comparison_data = []
        
        for ticker in tickers:
            analysis = self.analyze_fundamentals(ticker)
            if 'error' not in analysis:
                results[ticker] = analysis
                
                # Add to comparison table
                fundamental_score = analysis.get('fundamental_score', {})
                recommendation = analysis.get('recommendation', {})
                
                comparison_data.append({
                    'Ticker': ticker,
                    'Score': f"{fundamental_score.get('score_percentage', 0):.1f}%",
                    'Rating': fundamental_score.get('rating', 'N/A'),
                    'Recommendation': recommendation.get('recommendation', 'N/A'),
                    'P/E Ratio': analysis.get('valuation_metrics', {}).get('pe_ratio', 0),
                    'ROE': f"{analysis.get('financial_ratios', {}).get('roe', 0):.2%}",
                    'Debt/Equity': f"{analysis.get('debt_analysis', {}).get('debt_to_equity', 0):.2f}"
                })
        
        return {
            'comparison_table': pd.DataFrame(comparison_data),
            'detailed_results': results
        } 