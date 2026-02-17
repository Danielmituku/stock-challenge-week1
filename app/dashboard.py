"""
Stock Analysis Dashboard

An interactive Streamlit dashboard for exploring financial news sentiment
and stock price movements.

Run with: streamlit run app/dashboard.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import STOCK_TICKERS, TechnicalAnalysisConfig
from src.analysis.technical import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_daily_returns,
)
from src.analysis.sentiment import classify_sentiment

# Page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .positive {
        color: #2ecc71;
    }
    .negative {
        color: #e74c3c;
    }
    .neutral {
        color: #95a5a6;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_stock_data(ticker: str) -> pd.DataFrame:
    """Load stock data for a given ticker."""
    data_dir = Path(__file__).parent.parent / "data" / "Data" / "Data"
    file_path = data_dir / f"{ticker}_historical_data.csv"
    
    if not file_path.exists():
        # Try alternative path
        file_path = data_dir / f"{ticker}.csv"
    
    if not file_path.exists():
        st.error(f"Data file not found for {ticker}")
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df


@st.cache_data
def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for the stock data."""
    df = df.copy()
    
    # Moving averages
    df['SMA_20'] = calculate_sma(df['Close'], 20)
    df['SMA_50'] = calculate_sma(df['Close'], 50)
    df['SMA_200'] = calculate_sma(df['Close'], 200)
    df['EMA_12'] = calculate_ema(df['Close'], 12)
    df['EMA_26'] = calculate_ema(df['Close'], 26)
    
    # RSI
    df['RSI'] = calculate_rsi(df['Close'])
    
    # MACD
    macd, signal, hist = calculate_macd(df['Close'])
    df['MACD'] = macd
    df['MACD_Signal'] = signal
    df['MACD_Histogram'] = hist
    
    # Bollinger Bands
    upper, middle, lower = calculate_bollinger_bands(df['Close'])
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower
    
    # Daily returns
    df['Daily_Return'] = calculate_daily_returns(df['Close'])
    
    return df


@st.cache_data
def load_sentiment_data() -> pd.DataFrame:
    """Load pre-calculated sentiment data (simulated for demo)."""
    # In production, this would load actual sentiment data
    np.random.seed(42)
    
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
    
    data = []
    for ticker in STOCK_TICKERS:
        for date in dates[::5]:  # Every 5 days
            sentiment = np.random.uniform(-0.5, 0.5)
            data.append({
                'Date': date,
                'Ticker': ticker,
                'Sentiment': sentiment,
                'Category': classify_sentiment(sentiment),
                'Headlines': np.random.randint(1, 20),
            })
    
    return pd.DataFrame(data)


def create_price_chart(df: pd.DataFrame, ticker: str, show_ma: bool, show_bb: bool) -> go.Figure:
    """Create an interactive price chart with indicators."""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(f'{ticker} Stock Price', 'RSI', 'MACD')
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
        ),
        row=1, col=1
    )
    
    # Moving averages
    if show_ma:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['SMA_20'], name='SMA 20',
                      line=dict(color='orange', width=1)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['SMA_50'], name='SMA 50',
                      line=dict(color='blue', width=1)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['SMA_200'], name='SMA 200',
                      line=dict(color='red', width=1)),
            row=1, col=1
        )
    
    # Bollinger Bands
    if show_bb:
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Upper'], name='BB Upper',
                      line=dict(color='gray', width=1, dash='dot')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['BB_Lower'], name='BB Lower',
                      line=dict(color='gray', width=1, dash='dot'),
                      fill='tonexty', fillcolor='rgba(128, 128, 128, 0.1)'),
            row=1, col=1
        )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['RSI'], name='RSI',
                  line=dict(color='purple', width=1)),
        row=2, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    colors = ['green' if val >= 0 else 'red' for val in df['MACD_Histogram']]
    fig.add_trace(
        go.Bar(x=df['Date'], y=df['MACD_Histogram'], name='Histogram',
               marker_color=colors),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['MACD'], name='MACD',
                  line=dict(color='blue', width=1)),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['MACD_Signal'], name='Signal',
                  line=dict(color='orange', width=1)),
        row=3, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
    )
    
    return fig


def create_returns_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """Create a returns distribution chart."""
    returns = df['Daily_Return'].dropna()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Daily Returns Distribution', 'Cumulative Returns')
    )
    
    # Histogram
    fig.add_trace(
        go.Histogram(x=returns, nbinsx=50, name='Returns',
                    marker_color='steelblue'),
        row=1, col=1
    )
    
    # Cumulative returns
    cumulative = (1 + returns / 100).cumprod()
    fig.add_trace(
        go.Scatter(x=df['Date'][1:], y=cumulative, name='Cumulative',
                  line=dict(color='green', width=2)),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def create_sentiment_chart(sentiment_df: pd.DataFrame, ticker: str) -> go.Figure:
    """Create sentiment analysis chart."""
    ticker_data = sentiment_df[sentiment_df['Ticker'] == ticker].copy()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Sentiment Over Time', 'Sentiment Distribution'),
        specs=[[{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Time series
    fig.add_trace(
        go.Scatter(
            x=ticker_data['Date'],
            y=ticker_data['Sentiment'],
            mode='markers+lines',
            marker=dict(
                color=ticker_data['Sentiment'],
                colorscale='RdYlGn',
                size=8,
            ),
            name='Sentiment'
        ),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
    
    # Pie chart
    category_counts = ticker_data['Category'].value_counts()
    fig.add_trace(
        go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            marker_colors=['#2ecc71', '#e74c3c', '#95a5a6'],
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=400)
    
    return fig


def main():
    """Main dashboard function."""
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Financial News Sentiment & Technical Analysis")
    
    # Sidebar
    st.sidebar.header("Settings")
    
    # Stock selection
    selected_stock = st.sidebar.selectbox(
        "Select Stock",
        STOCK_TICKERS,
        index=0
    )
    
    # Date range
    st.sidebar.subheader("Date Range")
    
    # Indicator toggles
    st.sidebar.subheader("Technical Indicators")
    show_ma = st.sidebar.checkbox("Show Moving Averages", value=True)
    show_bb = st.sidebar.checkbox("Show Bollinger Bands", value=False)
    
    # Load data
    with st.spinner(f"Loading {selected_stock} data..."):
        df = load_stock_data(selected_stock)
        
        if df.empty:
            st.error("Could not load stock data. Please check if data files exist.")
            return
        
        df = calculate_indicators(df)
        sentiment_df = load_sentiment_data()
    
    # Filter by date range
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - pd.Timedelta(days=365), max_date),
        min_value=min_date,
        max_value=max_date,
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    
    # Key Metrics
    st.subheader(f"📊 Key Metrics for {selected_stock}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        latest_price = df['Close'].iloc[-1]
        st.metric("Latest Price", f"${latest_price:.2f}")
    
    with col2:
        daily_change = df['Daily_Return'].iloc[-1]
        st.metric(
            "Daily Change",
            f"{daily_change:.2f}%",
            delta=f"{daily_change:.2f}%"
        )
    
    with col3:
        volatility = df['Daily_Return'].std()
        st.metric("Volatility (Daily)", f"{volatility:.2f}%")
    
    with col4:
        rsi_value = df['RSI'].iloc[-1]
        rsi_status = "Overbought" if rsi_value > 70 else "Oversold" if rsi_value < 30 else "Neutral"
        st.metric("RSI", f"{rsi_value:.1f}", delta=rsi_status)
    
    with col5:
        total_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
        st.metric("Period Return", f"{total_return:.1f}%")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Price Chart",
        "📉 Returns Analysis", 
        "💬 Sentiment Analysis",
        "📋 Data Table"
    ])
    
    with tab1:
        st.subheader("Technical Analysis")
        price_chart = create_price_chart(df, selected_stock, show_ma, show_bb)
        st.plotly_chart(price_chart, use_container_width=True)
    
    with tab2:
        st.subheader("Returns Analysis")
        returns_chart = create_returns_chart(df, selected_stock)
        st.plotly_chart(returns_chart, use_container_width=True)
        
        # Statistics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Return Statistics")
            returns = df['Daily_Return'].dropna()
            stats_df = pd.DataFrame({
                'Metric': ['Mean Return', 'Std Dev', 'Min Return', 'Max Return', 'Positive Days %'],
                'Value': [
                    f"{returns.mean():.3f}%",
                    f"{returns.std():.3f}%",
                    f"{returns.min():.2f}%",
                    f"{returns.max():.2f}%",
                    f"{(returns > 0).mean() * 100:.1f}%"
                ]
            })
            st.dataframe(stats_df, hide_index=True)
    
    with tab3:
        st.subheader("Sentiment Analysis")
        sentiment_chart = create_sentiment_chart(sentiment_df, selected_stock)
        st.plotly_chart(sentiment_chart, use_container_width=True)
        
        # Sentiment summary
        ticker_sentiment = sentiment_df[sentiment_df['Ticker'] == selected_stock]
        avg_sentiment = ticker_sentiment['Sentiment'].mean()
        
        st.markdown(f"**Average Sentiment Score:** {avg_sentiment:.3f}")
        st.markdown(f"**Total Headlines Analyzed:** {ticker_sentiment['Headlines'].sum():,}")
    
    with tab4:
        st.subheader("Raw Data")
        st.dataframe(
            df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI', 'MACD']].tail(100),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Stock Analysis Dashboard** | Built with Streamlit | "
        "Data source: Historical stock prices | "
        "For educational purposes only"
    )


if __name__ == "__main__":
    main()
