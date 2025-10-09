# 🚀 AI Stock Advisor - System Architecture Diagram

## 📊 **High-Level Architecture**

```mermaid
graph TB
    subgraph "🌐 User Interface Layer"
        UI[Streamlit Web App]
        T1[📊 Stock Summary]
        T2[💡 Watchlist Suggestions]
        T3[📋 Compare Stocks]
        T4[💰 Portfolio Allocator]
        T5[🔬 Advanced Analysis]
    end
    
    subgraph "🤖 AI/ML Layer"
        GPT[OpenAI GPT-4 API]
        AI_ANALYSIS[AI Investment Analysis]
        RECOMMENDATIONS[Smart Recommendations]
    end
    
    subgraph "📡 Data Sources"
        YF[Yahoo Finance API]
        NEWS[NewsAPI]
        FH[Finnhub API]
        TRENDING[Trending Stocks API]
    end
    
    subgraph "⚙️ Processing Engine"
        TECH[Technical Analysis]
        FUND[Fundamental Analysis]
        RISK[Risk Management]
        BACKTEST[Backtesting Engine]
    end
    
    subgraph "💾 Data Processing"
        PANDAS[Pandas/NumPy]
        CACHE[Session State Cache]
        VALIDATION[Input Validation]
    end
    
    subgraph "☁️ Deployment"
        CLOUD[Streamlit Cloud]
        GIT[GitHub Repository]
        SECRETS[API Keys Management]
    end
    
    %% User Interface Connections
    UI --> T1
    UI --> T2
    UI --> T3
    UI --> T4
    UI --> T5
    
    %% AI Layer Connections
    T1 --> GPT
    T2 --> GPT
    T3 --> GPT
    T5 --> AI_ANALYSIS
    AI_ANALYSIS --> GPT
    GPT --> RECOMMENDATIONS
    
    %% Data Source Connections
    T1 --> YF
    T1 --> NEWS
    T2 --> TRENDING
    T3 --> YF
    T4 --> YF
    T5 --> YF
    T5 --> FH
    
    %% Processing Engine Connections
    T5 --> TECH
    T5 --> FUND
    T5 --> RISK
    T5 --> BACKTEST
    
    %% Data Processing Connections
    YF --> PANDAS
    NEWS --> PANDAS
    FH --> PANDAS
    TECH --> PANDAS
    FUND --> PANDAS
    RISK --> PANDAS
    BACKTEST --> PANDAS
    
    %% Cache and Validation
    PANDAS --> CACHE
    UI --> VALIDATION
    VALIDATION --> CACHE
    
    %% Deployment Connections
    CLOUD --> GIT
    CLOUD --> SECRETS
    CLOUD --> UI
```

## 🔄 **Data Flow Diagram**

```mermaid
flowchart TD
    START([User Input]) --> INPUT{Input Type}
    
    INPUT -->|Stock Symbol| SYMBOL[Validate Ticker]
    INPUT -->|Company Name| AUTO[Auto-Recognition]
    INPUT -->|Multiple Inputs| BATCH[Batch Processing]
    
    SYMBOL --> FETCH[Fetch Market Data]
    AUTO --> MAPPING[Company → Ticker Mapping]
    BATCH --> PARALLEL[Parallel Processing]
    
    MAPPING --> FETCH
    PARALLEL --> FETCH
    
    FETCH --> YF_DATA[Yahoo Finance Data]
    FETCH --> NEWS_DATA[News Headlines]
    FETCH --> EARNINGS_DATA[Earnings Reports]
    
    YF_DATA --> TECH_ANALYSIS[Technical Analysis]
    YF_DATA --> FUND_ANALYSIS[Fundamental Analysis]
    
    TECH_ANALYSIS --> RSI[RSI Calculation]
    TECH_ANALYSIS --> MA[Moving Averages]
    TECH_ANALYSIS --> BB[Bollinger Bands]
    TECH_ANALYSIS --> MACD[MACD Analysis]
    
    FUND_ANALYSIS --> PE[P/E Ratio]
    FUND_ANALYSIS --> ROE[ROE Analysis]
    FUND_ANALYSIS --> DEBT[Debt Analysis]
    FUND_ANALYSIS --> GROWTH[Growth Metrics]
    
    RSI --> COMBINE[Combine Signals]
    MA --> COMBINE
    BB --> COMBINE
    MACD --> COMBINE
    
    PE --> COMBINE
    ROE --> COMBINE
    DEBT --> COMBINE
    GROWTH --> COMBINE
    
    COMBINE --> RISK_MGMT[Risk Management]
    RISK_MGMT --> POSITION[Position Sizing]
    RISK_MGMT --> STOPLOSS[Stop-Loss Calculation]
    
    NEWS_DATA --> SENTIMENT[Sentiment Analysis]
    EARNINGS_DATA --> EARNINGS[Earnings Analysis]
    
    POSITION --> AI_INPUT[AI Analysis Input]
    STOPLOSS --> AI_INPUT
    SENTIMENT --> AI_INPUT
    EARNINGS --> AI_INPUT
    
    AI_INPUT --> GPT_API[GPT-4 API Call]
    GPT_API --> RECOMMENDATION[Investment Recommendation]
    
    RECOMMENDATION --> VISUALIZE[Data Visualization]
    VISUALIZE --> CHARTS[Interactive Charts]
    VISUALIZE --> TABLES[Data Tables]
    VISUALIZE --> METRICS[Performance Metrics]
    
    CHARTS --> OUTPUT[User Interface]
    TABLES --> OUTPUT
    METRICS --> OUTPUT
    
    OUTPUT --> USER([User Decision])
```

## 🏗️ **Component Architecture**

```mermaid
graph LR
    subgraph "Frontend Layer"
        A[Streamlit UI Components]
        B[Interactive Forms]
        C[Data Tables]
        D[Charts & Graphs]
        E[Progress Indicators]
    end
    
    subgraph "Business Logic Layer"
        F[Stock Analysis Engine]
        G[Portfolio Optimizer]
        H[Risk Calculator]
        I[Backtesting Module]
        J[Auto-Recognition Engine]
    end
    
    subgraph "Data Access Layer"
        K[Yahoo Finance Client]
        L[News API Client]
        M[Finnhub Client]
        N[Data Validator]
        O[Cache Manager]
    end
    
    subgraph "AI Integration Layer"
        P[OpenAI Client]
        Q[Prompt Engineering]
        R[Response Parser]
        S[Recommendation Engine]
    end
    
    A --> F
    B --> G
    C --> H
    D --> I
    E --> J
    
    F --> K
    G --> L
    H --> M
    I --> N
    J --> O
    
    K --> P
    L --> Q
    M --> R
    N --> S
    O --> P
```

## 📱 **User Journey Flow**

```mermaid
journey
    title User Journey Through AI Stock Advisor
    section Discovery
      Open App: 5: User
      View Header: 5: User
      Select Tab: 4: User
    section Stock Analysis
      Enter Ticker: 3: User
      Fetch Data: 5: System
      View Analysis: 5: User
      Read AI Insights: 5: User
    section Portfolio Planning
      Set Budget: 4: User
      Add Stocks: 3: User
      View Allocation: 5: User
      Optimize Portfolio: 4: User
    section Advanced Features
      Multi-Stock Analysis: 4: User
      Technical Indicators: 5: System
      Risk Assessment: 5: System
      Get Recommendations: 5: User
    section Decision Making
      Compare Options: 5: User
      Review AI Advice: 5: User
      Make Investment Decision: 5: User
```

## 🔧 **Technical Stack Diagram**

```mermaid
graph TB
    subgraph "🌐 Frontend"
        STREAMLIT[Streamlit Framework]
        PLOTLY[Plotly Charts]
        HTML[HTML/CSS Components]
    end
    
    subgraph "🐍 Backend"
        PYTHON[Python 3.x]
        PANDAS[Pandas DataFrames]
        NUMPY[NumPy Arrays]
        REQUESTS[HTTP Requests]
    end
    
    subgraph "🤖 AI/ML"
        OPENAI[OpenAI GPT-4]
        PROMPTS[Custom Prompts]
        PARSING[Response Parsing]
    end
    
    subgraph "📡 APIs"
        YFINANCE[Yahoo Finance]
        NEWSAPI[News API]
        FINNHUB[Finnhub API]
        TRENDING[Trending Stocks]
    end
    
    subgraph "💾 Data Storage"
        SESSION[Streamlit Session State]
        CACHE[In-Memory Cache]
        TEMP[Temporary Storage]
    end
    
    subgraph "☁️ Infrastructure"
        STREAMLIT_CLOUD[Streamlit Cloud]
        GITHUB[GitHub Repository]
        SECRETS[Environment Variables]
    end
    
    STREAMLIT --> PYTHON
    PLOTLY --> PANDAS
    HTML --> PYTHON
    
    PYTHON --> OPENAI
    PANDAS --> PROMPTS
    NUMPY --> PARSING
    REQUESTS --> OPENAI
    
    OPENAI --> YFINANCE
    PROMPTS --> NEWSAPI
    PARSING --> FINNHUB
    OPENAI --> TRENDING
    
    YFINANCE --> SESSION
    NEWSAPI --> CACHE
    FINNHUB --> TEMP
    TRENDING --> SESSION
    
    SESSION --> STREAMLIT_CLOUD
    CACHE --> GITHUB
    TEMP --> SECRETS
```

## 🎯 **Feature Module Breakdown**

```mermaid
graph TD
    subgraph "📊 Stock Summary Module"
        SS1[Trending Stocks Fetcher]
        SS2[Price Data Fetcher]
        SS3[Earnings Data Fetcher]
        SS4[News Headlines Fetcher]
        SS5[AI Summary Generator]
        SS6[Interactive Charts]
    end
    
    subgraph "💡 Watchlist Suggestions Module"
        WS1[Trending Stocks API]
        WS2[Batch Processing]
        WS3[Custom Prompt Engine]
        WS4[GPT-4 Integration]
        WS5[Response Formatting]
        WS6[Session State Management]
    end
    
    subgraph "📋 Compare Stocks Module"
        CS1[Multi-Stock Fetcher]
        CS2[Data Aggregation]
        CS3[Comparison Logic]
        CS4[Visualization Engine]
        CS5[Export Functionality]
    end
    
    subgraph "💰 Portfolio Allocator Module"
        PA1[Budget Input Handler]
        PA2[Sector Preference Engine]
        PA3[Auto-Recognition System]
        PA4[Allocation Algorithm]
        PA5[Fractional Share Calculator]
        PA6[Budget Optimization]
        PA7[Performance Metrics]
    end
    
    subgraph "🔬 Advanced Analysis Module"
        AA1[Technical Analysis Engine]
        AA2[Fundamental Analysis Engine]
        AA3[Risk Management Calculator]
        AA4[Backtesting Simulator]
        AA5[Multi-Ticker Processor]
        AA6[Ranking Algorithm]
        AA7[Recommendation Engine]
    end
    
    SS1 --> SS5
    SS2 --> SS6
    SS3 --> SS5
    SS4 --> SS5
    
    WS1 --> WS2
    WS2 --> WS3
    WS3 --> WS4
    WS4 --> WS5
    WS5 --> WS6
    
    CS1 --> CS2
    CS2 --> CS3
    CS3 --> CS4
    CS4 --> CS5
    
    PA1 --> PA2
    PA2 --> PA3
    PA3 --> PA4
    PA4 --> PA5
    PA5 --> PA6
    PA6 --> PA7
    
    AA1 --> AA6
    AA2 --> AA6
    AA3 --> AA6
    AA4 --> AA6
    AA5 --> AA6
    AA6 --> AA7
```

---

## 📝 **How to Use These Diagrams**

1. **Copy the Mermaid code** from any section above
2. **Paste into GitHub** - GitHub natively supports Mermaid diagrams
3. **Use in Markdown viewers** - Most modern Markdown viewers support Mermaid
4. **Online renderers** - Use [Mermaid Live Editor](https://mermaid.live/) to generate images
5. **Documentation** - Include in your project README or technical documentation

These diagrams comprehensively show your AI Stock Advisor's architecture, data flow, user journey, and technical components - perfect for technical presentations, documentation, and showcasing your system design skills!
