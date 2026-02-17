"""
Analysis module for sentiment and technical analysis.
"""

from .sentiment import (
    analyze_sentiment_textblob,
    analyze_sentiment_vader,
    analyze_sentiment_combined,
    classify_sentiment,
)
from .technical import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_atr,
    calculate_daily_returns,
    calculate_financial_metrics,
    calculate_all_indicators,
)
from .statistics import (
    gini_coefficient,
    identify_spikes,
    calculate_correlation,
)

__all__ = [
    # Sentiment analysis
    "analyze_sentiment_textblob",
    "analyze_sentiment_vader",
    "analyze_sentiment_combined",
    "classify_sentiment",
    # Technical analysis
    "calculate_sma",
    "calculate_ema",
    "calculate_rsi",
    "calculate_macd",
    "calculate_bollinger_bands",
    "calculate_atr",
    "calculate_daily_returns",
    "calculate_financial_metrics",
    "calculate_all_indicators",
    # Statistics
    "gini_coefficient",
    "identify_spikes",
    "calculate_correlation",
]
