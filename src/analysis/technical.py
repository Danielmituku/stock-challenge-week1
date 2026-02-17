"""
Technical analysis functions for stock data.
"""

from typing import Optional, Tuple, Dict, Any

import pandas as pd
import numpy as np

from ..config import (
    TechnicalAnalysisConfig,
    StockMetrics,
    RSI_PERIOD,
    RSI_OVERBOUGHT,
    RSI_OVERSOLD,
    MACD_FAST_PERIOD,
    MACD_SLOW_PERIOD,
    MACD_SIGNAL_PERIOD,
    SMA_PERIODS,
    EMA_PERIODS,
    BOLLINGER_PERIOD,
    BOLLINGER_STD,
    ATR_PERIOD,
)


def calculate_sma(
    prices: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calculate Simple Moving Average.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    period : int
        Number of periods for the moving average.
    
    Returns
    -------
    pd.Series
        Simple moving average values.
    
    Examples
    --------
    >>> sma_20 = calculate_sma(df['Close'], 20)
    """
    return prices.rolling(window=period).mean()


def calculate_ema(
    prices: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    period : int
        Number of periods for the moving average.
    
    Returns
    -------
    pd.Series
        Exponential moving average values.
    
    Examples
    --------
    >>> ema_12 = calculate_ema(df['Close'], 12)
    """
    return prices.ewm(span=period, adjust=False).mean()


def calculate_rsi(
    prices: pd.Series,
    period: int = RSI_PERIOD,
) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    RSI measures the speed and magnitude of price movements.
    Values above 70 indicate overbought conditions, below 30 indicate oversold.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    period : int, default 14
        Number of periods for RSI calculation.
    
    Returns
    -------
    pd.Series
        RSI values (0-100).
    
    Examples
    --------
    >>> rsi = calculate_rsi(df['Close'])
    >>> overbought = rsi > 70
    """
    delta = prices.diff()
    
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(
    prices: pd.Series,
    fast_period: int = MACD_FAST_PERIOD,
    slow_period: int = MACD_SLOW_PERIOD,
    signal_period: int = MACD_SIGNAL_PERIOD,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate Moving Average Convergence Divergence (MACD).
    
    MACD is a trend-following momentum indicator that shows the relationship
    between two moving averages of prices.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    fast_period : int, default 12
        Period for the fast EMA.
    slow_period : int, default 26
        Period for the slow EMA.
    signal_period : int, default 9
        Period for the signal line.
    
    Returns
    -------
    tuple
        (macd_line, signal_line, histogram)
    
    Examples
    --------
    >>> macd, signal, hist = calculate_macd(df['Close'])
    """
    ema_fast = calculate_ema(prices, fast_period)
    ema_slow = calculate_ema(prices, slow_period)
    
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(
    prices: pd.Series,
    period: int = BOLLINGER_PERIOD,
    std_dev: float = BOLLINGER_STD,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate Bollinger Bands.
    
    Bollinger Bands consist of a middle band (SMA) with upper and lower bands
    at standard deviation levels.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    period : int, default 20
        Period for the moving average.
    std_dev : float, default 2.0
        Number of standard deviations for the bands.
    
    Returns
    -------
    tuple
        (upper_band, middle_band, lower_band)
    
    Examples
    --------
    >>> upper, middle, lower = calculate_bollinger_bands(df['Close'])
    """
    middle_band = calculate_sma(prices, period)
    rolling_std = prices.rolling(window=period).std()
    
    upper_band = middle_band + (rolling_std * std_dev)
    lower_band = middle_band - (rolling_std * std_dev)
    
    return upper_band, middle_band, lower_band


def calculate_atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = ATR_PERIOD,
) -> pd.Series:
    """
    Calculate Average True Range (ATR).
    
    ATR is a volatility indicator that measures market volatility by
    decomposing the entire range of an asset price for that period.
    
    Parameters
    ----------
    high : pd.Series
        High prices.
    low : pd.Series
        Low prices.
    close : pd.Series
        Close prices.
    period : int, default 14
        Period for ATR calculation.
    
    Returns
    -------
    pd.Series
        ATR values.
    
    Examples
    --------
    >>> atr = calculate_atr(df['High'], df['Low'], df['Close'])
    """
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = abs(high - prev_close)
    tr3 = abs(low - prev_close)
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    return atr


def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate daily percentage returns.
    
    Parameters
    ----------
    prices : pd.Series
        Price series (typically Close prices).
    
    Returns
    -------
    pd.Series
        Daily returns as percentages.
    
    Examples
    --------
    >>> returns = calculate_daily_returns(df['Close'])
    """
    return prices.pct_change() * 100


def calculate_financial_metrics(
    df: pd.DataFrame,
    ticker: str,
    price_column: str = 'Close',
    risk_free_rate: float = 0.0,
) -> StockMetrics:
    """
    Calculate comprehensive financial metrics for a stock.
    
    Parameters
    ----------
    df : pd.DataFrame
        Stock price dataframe.
    ticker : str
        Stock ticker symbol.
    price_column : str, default 'Close'
        Column containing prices.
    risk_free_rate : float, default 0.0
        Annual risk-free rate for Sharpe ratio calculation.
    
    Returns
    -------
    StockMetrics
        Dataclass containing all calculated metrics.
    
    Examples
    --------
    >>> metrics = calculate_financial_metrics(df, 'AAPL')
    >>> print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
    """
    prices = df[price_column]
    returns = prices.pct_change().dropna()
    
    # Mean daily return
    mean_daily_return = returns.mean()
    
    # Volatility (annualized)
    daily_volatility = returns.std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    # Sharpe Ratio (annualized)
    excess_returns = returns - risk_free_rate / 252
    sharpe_ratio = (excess_returns.mean() / daily_volatility) * np.sqrt(252) if daily_volatility > 0 else 0
    
    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Total return
    total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100 if len(prices) > 0 else 0
    
    # Positive days percentage
    positive_days_pct = (returns > 0).mean() * 100
    
    return StockMetrics(
        ticker=ticker,
        mean_daily_return=mean_daily_return * 100,
        volatility=annualized_volatility * 100,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown * 100,
        total_return=total_return,
        positive_days_pct=positive_days_pct,
    )


def calculate_all_indicators(
    df: pd.DataFrame,
    config: Optional[TechnicalAnalysisConfig] = None,
) -> pd.DataFrame:
    """
    Calculate all technical indicators for a stock dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Stock price dataframe with columns: Open, High, Low, Close, Volume.
    config : TechnicalAnalysisConfig, optional
        Configuration for technical analysis parameters.
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with added indicator columns.
    
    Examples
    --------
    >>> df_with_indicators = calculate_all_indicators(df)
    """
    if config is None:
        config = TechnicalAnalysisConfig()
    
    df = df.copy()
    
    # Simple Moving Averages
    for period in config.sma_periods:
        df[f'SMA_{period}'] = calculate_sma(df['Close'], period)
    
    # Exponential Moving Averages
    for period in config.ema_periods:
        df[f'EMA_{period}'] = calculate_ema(df['Close'], period)
    
    # RSI
    df['RSI'] = calculate_rsi(df['Close'], config.rsi_period)
    
    # MACD
    macd, signal, hist = calculate_macd(
        df['Close'],
        config.macd_fast,
        config.macd_slow,
        config.macd_signal,
    )
    df['MACD'] = macd
    df['MACD_Signal'] = signal
    df['MACD_Histogram'] = hist
    
    # Bollinger Bands
    upper, middle, lower = calculate_bollinger_bands(
        df['Close'],
        config.bollinger_period,
        config.bollinger_std,
    )
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower
    
    # ATR
    df['ATR'] = calculate_atr(
        df['High'],
        df['Low'],
        df['Close'],
        config.atr_period,
    )
    
    # Daily Returns
    df['Daily_Return'] = calculate_daily_returns(df['Close'])
    
    return df
