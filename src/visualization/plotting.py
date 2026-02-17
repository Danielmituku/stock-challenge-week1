"""
Plotting functions for stock analysis visualization.
"""

from pathlib import Path
from typing import Optional, List, Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from ..config import VisualizationConfig, FIGURES_DIR


def setup_plotting_style(config: Optional[VisualizationConfig] = None) -> None:
    """
    Set up consistent plotting style across all visualizations.
    
    Parameters
    ----------
    config : VisualizationConfig, optional
        Configuration for visualization settings.
    
    Examples
    --------
    >>> setup_plotting_style()
    >>> # Or with custom config
    >>> config = VisualizationConfig(style='ggplot')
    >>> setup_plotting_style(config)
    """
    if config is None:
        config = VisualizationConfig()
    
    try:
        plt.style.use(config.style)
    except OSError:
        plt.style.use('seaborn-v0_8-whitegrid')
    
    sns.set_palette(config.palette)
    plt.rcParams['figure.figsize'] = config.figsize
    plt.rcParams['figure.dpi'] = config.dpi
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    
    print("Plotting style configured")


def save_figure(
    fig: plt.Figure,
    filename: str,
    figures_dir: Optional[Union[str, Path]] = None,
    dpi: int = 300,
) -> Path:
    """
    Save a figure to the figures directory.
    
    Parameters
    ----------
    fig : plt.Figure
        Matplotlib figure to save.
    filename : str
        Name of the file (with extension).
    figures_dir : str or Path, optional
        Directory to save figures. Defaults to notebooks/figures/.
    dpi : int, default 300
        Resolution for saved figure.
    
    Returns
    -------
    Path
        Path to the saved figure.
    
    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3])
    >>> path = save_figure(fig, 'my_plot.png')
    """
    if figures_dir is None:
        figures_dir = FIGURES_DIR
    
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = figures_dir / filename
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Saved figure to {filepath}")
    
    return filepath


def plot_stock_with_indicators(
    df: pd.DataFrame,
    ticker: str,
    indicators: Optional[List[str]] = None,
    figsize: tuple = (14, 10),
    save: bool = False,
    figures_dir: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """
    Create a comprehensive stock chart with technical indicators.
    
    Parameters
    ----------
    df : pd.DataFrame
        Stock dataframe with indicators calculated.
    ticker : str
        Stock ticker symbol for the title.
    indicators : list of str, optional
        List of indicators to include. Options: 'sma', 'ema', 'bollinger', 'rsi', 'macd'.
        If None, shows all available.
    figsize : tuple, default (14, 10)
        Figure size.
    save : bool, default False
        If True, save the figure.
    figures_dir : str or Path, optional
        Directory to save figures.
    
    Returns
    -------
    plt.Figure
        The matplotlib figure.
    
    Examples
    --------
    >>> fig = plot_stock_with_indicators(df, 'AAPL')
    >>> plt.show()
    """
    if indicators is None:
        indicators = ['sma', 'ema', 'bollinger', 'rsi', 'macd']
    
    num_subplots = 1 + ('rsi' in indicators) + ('macd' in indicators)
    
    fig, axes = plt.subplots(num_subplots, 1, figsize=figsize, 
                             gridspec_kw={'height_ratios': [3] + [1] * (num_subplots - 1)})
    
    if num_subplots == 1:
        axes = [axes]
    
    ax_price = axes[0]
    
    # Price and moving averages
    ax_price.plot(df['Date'], df['Close'], label='Close', linewidth=1.5, color='black')
    
    if 'sma' in indicators:
        for col in df.columns:
            if col.startswith('SMA_'):
                ax_price.plot(df['Date'], df[col], label=col, linewidth=1, alpha=0.7)
    
    if 'ema' in indicators:
        for col in df.columns:
            if col.startswith('EMA_'):
                ax_price.plot(df['Date'], df[col], label=col, linewidth=1, linestyle='--', alpha=0.7)
    
    if 'bollinger' in indicators and 'BB_Upper' in df.columns:
        ax_price.fill_between(df['Date'], df['BB_Lower'], df['BB_Upper'], 
                             alpha=0.2, color='gray', label='Bollinger Bands')
    
    ax_price.set_title(f'{ticker} Stock Price with Technical Indicators')
    ax_price.set_ylabel('Price ($)')
    ax_price.legend(loc='upper left', fontsize=8)
    ax_price.grid(True, alpha=0.3)
    
    # RSI
    subplot_idx = 1
    if 'rsi' in indicators and 'RSI' in df.columns:
        ax_rsi = axes[subplot_idx]
        ax_rsi.plot(df['Date'], df['RSI'], label='RSI', color='purple', linewidth=1)
        ax_rsi.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Overbought (70)')
        ax_rsi.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Oversold (30)')
        ax_rsi.fill_between(df['Date'], 30, 70, alpha=0.1, color='gray')
        ax_rsi.set_ylabel('RSI')
        ax_rsi.set_ylim(0, 100)
        ax_rsi.legend(loc='upper left', fontsize=8)
        ax_rsi.grid(True, alpha=0.3)
        subplot_idx += 1
    
    # MACD
    if 'macd' in indicators and 'MACD' in df.columns:
        ax_macd = axes[subplot_idx]
        ax_macd.plot(df['Date'], df['MACD'], label='MACD', color='blue', linewidth=1)
        ax_macd.plot(df['Date'], df['MACD_Signal'], label='Signal', color='orange', linewidth=1)
        
        colors = ['green' if val >= 0 else 'red' for val in df['MACD_Histogram']]
        ax_macd.bar(df['Date'], df['MACD_Histogram'], color=colors, alpha=0.5, label='Histogram')
        
        ax_macd.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax_macd.set_ylabel('MACD')
        ax_macd.set_xlabel('Date')
        ax_macd.legend(loc='upper left', fontsize=8)
        ax_macd.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save:
        save_figure(fig, f'{ticker}_technical_analysis.png', figures_dir)
    
    return fig


def plot_sentiment_distribution(
    df: pd.DataFrame,
    sentiment_column: str = 'sentiment_combined',
    category_column: str = 'sentiment_category',
    figsize: tuple = (12, 5),
    save: bool = False,
    filename: str = 'sentiment_distribution.png',
    figures_dir: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """
    Plot sentiment distribution and category breakdown.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with sentiment scores.
    sentiment_column : str, default 'sentiment_combined'
        Column containing sentiment scores.
    category_column : str, default 'sentiment_category'
        Column containing sentiment categories.
    figsize : tuple, default (12, 5)
        Figure size.
    save : bool, default False
        If True, save the figure.
    filename : str, default 'sentiment_distribution.png'
        Filename for saving.
    figures_dir : str or Path, optional
        Directory to save figures.
    
    Returns
    -------
    plt.Figure
        The matplotlib figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram of sentiment scores
    axes[0].hist(df[sentiment_column].dropna(), bins=50, edgecolor='black', alpha=0.7)
    axes[0].axvline(x=0, color='red', linestyle='--', label='Neutral (0)')
    axes[0].set_xlabel('Sentiment Score')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of Sentiment Scores')
    axes[0].legend()
    
    # Pie chart of categories
    if category_column in df.columns:
        category_counts = df[category_column].value_counts()
        colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
        pie_colors = [colors.get(cat, '#3498db') for cat in category_counts.index]
        
        axes[1].pie(category_counts.values, labels=category_counts.index, 
                   autopct='%1.1f%%', colors=pie_colors, startangle=90)
        axes[1].set_title('Sentiment Category Distribution')
    
    plt.tight_layout()
    
    if save:
        save_figure(fig, filename, figures_dir)
    
    return fig


def plot_correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    title: str = 'Correlation Matrix',
    figsize: tuple = (10, 8),
    cmap: str = 'RdYlGn',
    save: bool = False,
    filename: str = 'correlation_heatmap.png',
    figures_dir: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """
    Plot a correlation matrix as a heatmap.
    
    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Square correlation matrix.
    title : str, default 'Correlation Matrix'
        Plot title.
    figsize : tuple, default (10, 8)
        Figure size.
    cmap : str, default 'RdYlGn'
        Colormap for the heatmap.
    save : bool, default False
        If True, save the figure.
    filename : str, default 'correlation_heatmap.png'
        Filename for saving.
    figures_dir : str or Path, optional
        Directory to save figures.
    
    Returns
    -------
    plt.Figure
        The matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
    sns.heatmap(
        correlation_matrix,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap=cmap,
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        ax=ax,
    )
    
    ax.set_title(title, fontsize=14)
    plt.tight_layout()
    
    if save:
        save_figure(fig, filename, figures_dir)
    
    return fig
