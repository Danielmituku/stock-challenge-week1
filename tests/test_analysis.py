"""
Unit tests for analysis module.
"""

import pytest
import pandas as pd
import numpy as np

from src.analysis.sentiment import (
    analyze_sentiment_textblob,
    analyze_sentiment_vader,
    classify_sentiment,
)
from src.analysis.technical import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_daily_returns,
)
from src.analysis.statistics import (
    gini_coefficient,
    identify_spikes,
    calculate_correlation,
    extract_email_domain,
)


class TestSentimentAnalysis:
    """Tests for sentiment analysis functions."""
    
    def test_textblob_positive_sentiment(self):
        """Test TextBlob with positive text."""
        score = analyze_sentiment_textblob("This is excellent and amazing news!")
        assert score > 0
    
    def test_textblob_negative_sentiment(self):
        """Test TextBlob with negative text."""
        score = analyze_sentiment_textblob("This is terrible and horrible news!")
        assert score < 0
    
    def test_textblob_neutral_sentiment(self):
        """Test TextBlob with neutral text."""
        score = analyze_sentiment_textblob("The meeting is scheduled for tomorrow.")
        # Neutral text should be close to 0
        assert -0.3 < score < 0.3
    
    def test_textblob_empty_string(self):
        """Test TextBlob with empty string."""
        score = analyze_sentiment_textblob("")
        assert score == 0.0
    
    def test_vader_positive_sentiment(self):
        """Test VADER with positive text."""
        score = analyze_sentiment_vader("This is great news! Stock soaring with excellent profits!")
        assert score > 0
    
    def test_vader_negative_sentiment(self):
        """Test VADER with negative text."""
        score = analyze_sentiment_vader("Company reports massive losses!")
        assert score < 0
    
    def test_vader_empty_string(self):
        """Test VADER with empty string."""
        score = analyze_sentiment_vader("")
        assert score == 0.0
    
    def test_classify_sentiment_positive(self):
        """Test sentiment classification for positive scores."""
        assert classify_sentiment(0.5) == "positive"
        assert classify_sentiment(0.1) == "positive"
    
    def test_classify_sentiment_negative(self):
        """Test sentiment classification for negative scores."""
        assert classify_sentiment(-0.5) == "negative"
        assert classify_sentiment(-0.1) == "negative"
    
    def test_classify_sentiment_neutral(self):
        """Test sentiment classification for neutral scores."""
        assert classify_sentiment(0.0) == "neutral"
        assert classify_sentiment(0.03) == "neutral"
        assert classify_sentiment(-0.03) == "neutral"


class TestTechnicalAnalysis:
    """Tests for technical analysis functions."""
    
    @pytest.fixture
    def sample_prices(self):
        """Create sample price data for testing."""
        np.random.seed(42)
        prices = pd.Series(100 + np.cumsum(np.random.randn(100)))
        return prices
    
    def test_calculate_sma(self, sample_prices):
        """Test Simple Moving Average calculation."""
        sma = calculate_sma(sample_prices, 20)
        
        # First 19 values should be NaN
        assert sma[:19].isna().all()
        
        # After that, values should exist
        assert not sma[19:].isna().any()
        
        # SMA of period 20 at index 19 should be mean of first 20 values
        expected = sample_prices[:20].mean()
        assert abs(sma.iloc[19] - expected) < 0.001
    
    def test_calculate_ema(self, sample_prices):
        """Test Exponential Moving Average calculation."""
        ema = calculate_ema(sample_prices, 12)
        
        # EMA should have values from the start
        assert not ema.isna().all()
        
        # EMA should smooth the data
        assert ema.std() < sample_prices.std()
    
    def test_calculate_rsi(self, sample_prices):
        """Test RSI calculation."""
        rsi = calculate_rsi(sample_prices, 14)
        
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()
    
    def test_calculate_macd(self, sample_prices):
        """Test MACD calculation."""
        macd, signal, histogram = calculate_macd(sample_prices)
        
        # All outputs should have same length as input
        assert len(macd) == len(sample_prices)
        assert len(signal) == len(sample_prices)
        assert len(histogram) == len(sample_prices)
        
        # Histogram should be MACD - Signal
        valid_idx = ~(macd.isna() | signal.isna())
        np.testing.assert_array_almost_equal(
            histogram[valid_idx],
            (macd - signal)[valid_idx],
            decimal=10
        )
    
    def test_calculate_daily_returns(self, sample_prices):
        """Test daily returns calculation."""
        returns = calculate_daily_returns(sample_prices)
        
        # First return should be NaN
        assert pd.isna(returns.iloc[0])
        
        # Manually calculate second return
        expected = ((sample_prices.iloc[1] - sample_prices.iloc[0]) / sample_prices.iloc[0]) * 100
        assert abs(returns.iloc[1] - expected) < 0.001


class TestStatistics:
    """Tests for statistical functions."""
    
    def test_gini_coefficient_equal(self):
        """Test Gini coefficient with equal values."""
        values = np.array([10, 10, 10, 10, 10])
        gini = gini_coefficient(values)
        # Perfect equality should give Gini close to 0
        assert abs(gini) < 0.1
    
    def test_gini_coefficient_unequal(self):
        """Test Gini coefficient with unequal values."""
        values = np.array([1, 1, 1, 1, 100])
        gini = gini_coefficient(values)
        # High inequality should give Gini closer to 1
        assert gini > 0.5
    
    def test_identify_spikes(self):
        """Test spike identification."""
        data = pd.Series([10, 11, 9, 10, 50, 10, 12])
        spikes = identify_spikes(data, threshold_std=2)
        
        # The value 50 should be identified as a spike
        assert len(spikes) == 1
        assert 50 in spikes.values
    
    def test_identify_spikes_no_spikes(self):
        """Test spike identification with no spikes."""
        data = pd.Series([10, 11, 10, 11, 10, 11, 10])
        spikes = identify_spikes(data, threshold_std=2)
        
        assert len(spikes) == 0
    
    def test_calculate_correlation(self):
        """Test correlation calculation."""
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([2, 4, 6, 8, 10])
        
        corr, p_value, n = calculate_correlation(x, y)
        
        # Perfect positive correlation
        assert abs(corr - 1.0) < 0.001
        assert p_value < 0.05
        assert n == 5
    
    def test_calculate_correlation_negative(self):
        """Test negative correlation calculation."""
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([10, 8, 6, 4, 2])
        
        corr, p_value, n = calculate_correlation(x, y)
        
        # Perfect negative correlation
        assert abs(corr + 1.0) < 0.001
    
    def test_calculate_correlation_insufficient_data(self):
        """Test correlation with insufficient data."""
        x = pd.Series([1, 2])
        y = pd.Series([2, 4])
        
        corr, p_value, n = calculate_correlation(x, y)
        
        # Should return default values for insufficient data
        assert n == 2
    
    def test_extract_email_domain(self):
        """Test email domain extraction."""
        assert extract_email_domain("analyst@bloomberg.com") == "bloomberg.com"
        assert extract_email_domain("john.doe@finance.reuters.net") == "finance.reuters.net"
        assert extract_email_domain("Not an email") is None
        assert extract_email_domain("") is None
