"""
Pytest configuration and shared fixtures.
"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_news_df():
    """Create a sample news dataframe for testing."""
    return pd.DataFrame({
        'headline': [
            'Apple stock price rises on strong earnings',
            'Amazon reports record quarterly profits',
            'Google faces regulatory challenges',
            'Microsoft announces new product launch',
            'Tesla stock drops on production concerns',
        ],
        'url': [
            'http://example.com/article1',
            'http://example.com/article2',
            'http://example.com/article3',
            'http://example.com/article4',
            'http://example.com/article5',
        ],
        'publisher': [
            'Bloomberg',
            'Reuters',
            'CNBC',
            'Bloomberg',
            'Reuters',
        ],
        'date': pd.to_datetime([
            '2024-01-15 10:30:00',
            '2024-01-15 11:00:00',
            '2024-01-15 14:00:00',
            '2024-01-16 09:00:00',
            '2024-01-16 10:30:00',
        ]),
        'stock': ['AAPL', 'AMZN', 'GOOG', 'MSFT', 'TSLA'],
    })


@pytest.fixture
def sample_stock_df():
    """Create a sample stock price dataframe for testing."""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    # Generate realistic-looking price data
    base_price = 150.0
    returns = np.random.randn(100) * 0.02  # 2% daily volatility
    prices = base_price * (1 + returns).cumprod()
    
    return pd.DataFrame({
        'Date': dates,
        'Open': prices * (1 + np.random.randn(100) * 0.005),
        'High': prices * (1 + abs(np.random.randn(100) * 0.01)),
        'Low': prices * (1 - abs(np.random.randn(100) * 0.01)),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, 100),
    })


@pytest.fixture
def sample_prices():
    """Create a simple price series for testing."""
    np.random.seed(42)
    return pd.Series(100 + np.cumsum(np.random.randn(100)))


@pytest.fixture
def sample_returns():
    """Create a simple returns series for testing."""
    np.random.seed(42)
    return pd.Series(np.random.randn(100) * 2)  # 2% std daily returns
