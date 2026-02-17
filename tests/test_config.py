"""
Unit tests for configuration module.
"""

import pytest
from src.config import (
    DataConfig,
    TechnicalAnalysisConfig,
    SentimentConfig,
    QualityReport,
    StockMetrics,
    STOCK_TICKERS,
    RSI_PERIOD,
    MACD_FAST_PERIOD,
)


class TestDataConfig:
    """Tests for DataConfig dataclass."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = DataConfig()
        assert config.sample_size is None
        assert config.remove_duplicates is True
        assert config.handle_missing == "report"
        assert config.fix_dates is True
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = DataConfig(
            sample_size=1000,
            remove_duplicates=False,
            handle_missing="drop",
        )
        assert config.sample_size == 1000
        assert config.remove_duplicates is False
        assert config.handle_missing == "drop"
    
    def test_invalid_handle_missing(self):
        """Test that invalid handle_missing raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DataConfig(handle_missing="invalid")
        assert "handle_missing must be one of" in str(exc_info.value)


class TestTechnicalAnalysisConfig:
    """Tests for TechnicalAnalysisConfig dataclass."""
    
    def test_default_values(self):
        """Test default technical analysis configuration."""
        config = TechnicalAnalysisConfig()
        assert config.rsi_period == RSI_PERIOD
        assert config.macd_fast == MACD_FAST_PERIOD
        assert config.rsi_overbought == 70.0
        assert config.rsi_oversold == 30.0
    
    def test_sma_periods_are_copied(self):
        """Test that sma_periods list is properly copied."""
        config1 = TechnicalAnalysisConfig()
        config2 = TechnicalAnalysisConfig()
        
        config1.sma_periods.append(100)
        
        # config2 should not be affected
        assert 100 not in config2.sma_periods


class TestQualityReport:
    """Tests for QualityReport dataclass."""
    
    def test_missing_percentage(self):
        """Test missing percentage calculation."""
        report = QualityReport(
            total_rows=100,
            missing_values={'col1': 10, 'col2': 5},
        )
        assert report.missing_percentage == 15.0
    
    def test_missing_percentage_empty(self):
        """Test missing percentage with no missing values."""
        report = QualityReport(total_rows=100)
        assert report.missing_percentage == 0.0
    
    def test_duplicate_percentage(self):
        """Test duplicate percentage calculation."""
        report = QualityReport(
            total_rows=100,
            duplicate_rows=25,
        )
        assert report.duplicate_percentage == 25.0
    
    def test_zero_rows(self):
        """Test percentages with zero rows."""
        report = QualityReport(total_rows=0)
        assert report.missing_percentage == 0.0
        assert report.duplicate_percentage == 0.0


class TestStockMetrics:
    """Tests for StockMetrics dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        metrics = StockMetrics(
            ticker="AAPL",
            mean_daily_return=0.15,
            volatility=25.0,
            sharpe_ratio=1.5,
            max_drawdown=-15.0,
            total_return=150.0,
            positive_days_pct=55.0,
        )
        
        result = metrics.to_dict()
        
        assert result["ticker"] == "AAPL"
        assert result["mean_daily_return"] == 0.15
        assert result["volatility"] == 25.0
        assert result["sharpe_ratio"] == 1.5


class TestConstants:
    """Tests for module constants."""
    
    def test_stock_tickers(self):
        """Test stock tickers list."""
        expected_tickers = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA"]
        assert STOCK_TICKERS == expected_tickers
    
    def test_rsi_period(self):
        """Test RSI period constant."""
        assert RSI_PERIOD == 14
