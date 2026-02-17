"""
Statistical analysis functions.
"""

from typing import Tuple, Optional
import re

import pandas as pd
import numpy as np
from scipy import stats


def gini_coefficient(values: np.ndarray) -> float:
    """
    Calculate Gini coefficient to measure inequality.
    
    The Gini coefficient ranges from 0 (perfect equality) to 1 (perfect inequality).
    Useful for measuring concentration in publisher activity, stock coverage, etc.
    
    Parameters
    ----------
    values : array-like
        Values to calculate Gini coefficient for.
    
    Returns
    -------
    float
        Gini coefficient between 0 and 1.
    
    Examples
    --------
    >>> articles_per_publisher = df['publisher'].value_counts().values
    >>> gini = gini_coefficient(articles_per_publisher)
    >>> print(f"Gini coefficient: {gini:.3f}")
    """
    values = np.asarray(values, dtype=float)
    values = values[values > 0]  # Remove zeros
    
    if len(values) == 0:
        return 0.0
    
    sorted_values = np.sort(values)
    n = len(sorted_values)
    index = np.arange(1, n + 1)
    
    return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n


def identify_spikes(
    series: pd.Series,
    threshold_std: float = 2.0,
) -> pd.Series:
    """
    Identify spikes in a time series.
    
    A spike is defined as a value more than threshold_std standard deviations
    above the mean.
    
    Parameters
    ----------
    series : pd.Series
        Time series data.
    threshold_std : float, default 2.0
        Number of standard deviations above mean to consider a spike.
    
    Returns
    -------
    pd.Series
        Series containing only the spike values.
    
    Examples
    --------
    >>> daily_counts = df.groupby('date_only').size()
    >>> spikes = identify_spikes(daily_counts)
    >>> print(f"Found {len(spikes)} spike days")
    """
    mean = series.mean()
    std = series.std()
    threshold = mean + threshold_std * std
    
    spikes = series[series > threshold]
    return spikes


def calculate_correlation(
    x: pd.Series,
    y: pd.Series,
    method: str = 'pearson',
) -> Tuple[float, float, int]:
    """
    Calculate correlation coefficient with statistical significance.
    
    Parameters
    ----------
    x : pd.Series
        First variable.
    y : pd.Series
        Second variable.
    method : str, default 'pearson'
        Correlation method: 'pearson', 'spearman', or 'kendall'.
    
    Returns
    -------
    tuple
        (correlation_coefficient, p_value, sample_size)
    
    Notes
    -----
    - Automatically aligns the two series by their index
    - Drops any NaN values before calculation
    - Returns (0, 1, 0) if insufficient data
    
    Examples
    --------
    >>> corr, p_val, n = calculate_correlation(sentiment, returns)
    >>> if p_val < 0.05:
    ...     print(f"Significant correlation: {corr:.3f}")
    """
    # Align by index and drop NaN
    aligned = pd.concat([x, y], axis=1).dropna()
    
    if len(aligned) < 3:
        return 0.0, 1.0, len(aligned)
    
    x_aligned = aligned.iloc[:, 0]
    y_aligned = aligned.iloc[:, 1]
    
    if method == 'pearson':
        corr, p_value = stats.pearsonr(x_aligned, y_aligned)
    elif method == 'spearman':
        corr, p_value = stats.spearmanr(x_aligned, y_aligned)
    elif method == 'kendall':
        corr, p_value = stats.kendalltau(x_aligned, y_aligned)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'pearson', 'spearman', or 'kendall'.")
    
    return corr, p_value, len(aligned)


def extract_email_domain(publisher: str) -> Optional[str]:
    """
    Extract email domain from publisher name if it's an email address.
    
    Parameters
    ----------
    publisher : str
        Publisher name (may be email address).
    
    Returns
    -------
    str or None
        Domain if email found, None otherwise.
    
    Examples
    --------
    >>> domain = extract_email_domain("analyst@bloomberg.com")
    >>> print(domain)  # 'bloomberg.com'
    """
    email_pattern = r'([a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))'
    match = re.search(email_pattern, str(publisher))
    if match:
        return match.group(2)  # Return the domain part
    return None


def calculate_summary_statistics(series: pd.Series) -> dict:
    """
    Calculate comprehensive summary statistics for a series.
    
    Parameters
    ----------
    series : pd.Series
        Numeric series to analyze.
    
    Returns
    -------
    dict
        Dictionary containing:
        - count, mean, std, min, max
        - median, q1, q3, iqr
        - skewness, kurtosis
    
    Examples
    --------
    >>> stats = calculate_summary_statistics(df['headline_length'])
    >>> print(f"Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}")
    """
    return {
        'count': int(series.count()),
        'mean': float(series.mean()),
        'std': float(series.std()),
        'min': float(series.min()),
        'max': float(series.max()),
        'median': float(series.median()),
        'q1': float(series.quantile(0.25)),
        'q3': float(series.quantile(0.75)),
        'iqr': float(series.quantile(0.75) - series.quantile(0.25)),
        'skewness': float(series.skew()),
        'kurtosis': float(series.kurtosis()),
    }
