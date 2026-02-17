"""
Stock Challenge - Financial News Sentiment Analysis

A comprehensive analysis of financial news sentiment and its correlation
with stock price movements.

Modules
-------
config
    Configuration dataclasses and constants.
data
    Data loading and preprocessing functions.
analysis
    Sentiment analysis and technical indicators.
visualization
    Plotting and charting utilities.
"""

from . import config
from . import data
from . import analysis
from . import visualization

__version__ = "1.0.0"
__author__ = "Stock Challenge Team"

__all__ = [
    "config",
    "data",
    "analysis",
    "visualization",
]
