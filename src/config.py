"""
Configuration module for Stock Challenge project.

This module contains dataclasses and constants used throughout the project.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "notebooks" / "figures"

# Stock tickers analyzed
STOCK_TICKERS: List[str] = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA"]

# Technical analysis constants
RSI_PERIOD: int = 14
RSI_OVERBOUGHT: float = 70.0
RSI_OVERSOLD: float = 30.0

MACD_FAST_PERIOD: int = 12
MACD_SLOW_PERIOD: int = 26
MACD_SIGNAL_PERIOD: int = 9

SMA_PERIODS: List[int] = [20, 50, 200]
EMA_PERIODS: List[int] = [12, 26]

BOLLINGER_PERIOD: int = 20
BOLLINGER_STD: float = 2.0

ATR_PERIOD: int = 14

# Sentiment analysis thresholds
SENTIMENT_POSITIVE_THRESHOLD: float = 0.05
SENTIMENT_NEGATIVE_THRESHOLD: float = -0.05

# Visualization constants
FIGURE_DPI: int = 300
DEFAULT_FIGSIZE: tuple = (12, 8)


@dataclass
class DataConfig:
    """Configuration for data loading and preprocessing."""
    
    file_path: str = str(DATA_DIR / "raw_analyst_ratings.csv")
    sample_size: Optional[int] = None
    remove_duplicates: bool = True
    handle_missing: str = "report"  # 'report', 'drop', or 'fill'
    fix_dates: bool = True
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        valid_missing_handlers = ["report", "drop", "fill"]
        if self.handle_missing not in valid_missing_handlers:
            raise ValueError(
                f"handle_missing must be one of {valid_missing_handlers}, "
                f"got '{self.handle_missing}'"
            )


@dataclass
class TechnicalAnalysisConfig:
    """Configuration for technical analysis calculations."""
    
    rsi_period: int = RSI_PERIOD
    rsi_overbought: float = RSI_OVERBOUGHT
    rsi_oversold: float = RSI_OVERSOLD
    
    macd_fast: int = MACD_FAST_PERIOD
    macd_slow: int = MACD_SLOW_PERIOD
    macd_signal: int = MACD_SIGNAL_PERIOD
    
    sma_periods: List[int] = field(default_factory=lambda: SMA_PERIODS.copy())
    ema_periods: List[int] = field(default_factory=lambda: EMA_PERIODS.copy())
    
    bollinger_period: int = BOLLINGER_PERIOD
    bollinger_std: float = BOLLINGER_STD
    
    atr_period: int = ATR_PERIOD


@dataclass
class SentimentConfig:
    """Configuration for sentiment analysis."""
    
    positive_threshold: float = SENTIMENT_POSITIVE_THRESHOLD
    negative_threshold: float = SENTIMENT_NEGATIVE_THRESHOLD
    use_vader: bool = True
    use_textblob: bool = True
    combine_scores: bool = True


@dataclass
class VisualizationConfig:
    """Configuration for visualizations."""
    
    dpi: int = FIGURE_DPI
    figsize: tuple = DEFAULT_FIGSIZE
    style: str = "seaborn-v0_8-darkgrid"
    palette: str = "husl"
    save_figures: bool = True
    figures_dir: Path = FIGURES_DIR


@dataclass 
class QualityReport:
    """Data quality report structure."""
    
    total_rows: int = 0
    missing_values: dict = field(default_factory=dict)
    duplicate_rows: int = 0
    duplicate_headlines: int = 0
    duplicate_urls: int = 0
    valid_dates: int = 0
    invalid_dates: int = 0
    outliers: dict = field(default_factory=dict)
    
    @property
    def missing_percentage(self) -> float:
        """Calculate overall missing value percentage."""
        if self.total_rows == 0:
            return 0.0
        total_missing = sum(self.missing_values.values()) if self.missing_values else 0
        return (total_missing / self.total_rows) * 100
    
    @property
    def duplicate_percentage(self) -> float:
        """Calculate duplicate row percentage."""
        if self.total_rows == 0:
            return 0.0
        return (self.duplicate_rows / self.total_rows) * 100


@dataclass
class StockMetrics:
    """Financial metrics for a stock."""
    
    ticker: str
    mean_daily_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    total_return: float
    positive_days_pct: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "ticker": self.ticker,
            "mean_daily_return": self.mean_daily_return,
            "volatility": self.volatility,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "total_return": self.total_return,
            "positive_days_pct": self.positive_days_pct,
        }
