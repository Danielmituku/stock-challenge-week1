"""
Sentiment analysis functions using TextBlob and VADER.
"""

from typing import Optional, Tuple, Union

import pandas as pd
import numpy as np

from ..config import SentimentConfig, SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEGATIVE_THRESHOLD


def analyze_sentiment_textblob(text: str) -> float:
    """
    Analyze sentiment using TextBlob.
    
    Parameters
    ----------
    text : str
        Text to analyze.
    
    Returns
    -------
    float
        Polarity score from -1 (negative) to 1 (positive).
    
    Examples
    --------
    >>> score = analyze_sentiment_textblob("This is great news!")
    >>> print(f"Sentiment: {score:.3f}")
    """
    try:
        from textblob import TextBlob
    except ImportError:
        raise ImportError("TextBlob not installed. Install with: pip install textblob")
    
    if not isinstance(text, str) or not text.strip():
        return 0.0
    
    blob = TextBlob(text)
    return blob.sentiment.polarity


def analyze_sentiment_vader(text: str) -> float:
    """
    Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    
    VADER is specifically attuned to sentiments expressed in social media and
    works well for financial text.
    
    Parameters
    ----------
    text : str
        Text to analyze.
    
    Returns
    -------
    float
        Compound score from -1 (negative) to 1 (positive).
    
    Examples
    --------
    >>> score = analyze_sentiment_vader("Stock price target raised!")
    >>> print(f"Sentiment: {score:.3f}")
    """
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    except ImportError:
        raise ImportError(
            "vaderSentiment not installed. Install with: pip install vaderSentiment"
        )
    
    if not isinstance(text, str) or not text.strip():
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores['compound']


def analyze_sentiment_combined(
    text: str,
    config: Optional[SentimentConfig] = None,
) -> Tuple[float, float, float]:
    """
    Analyze sentiment using both TextBlob and VADER, returning combined score.
    
    Parameters
    ----------
    text : str
        Text to analyze.
    config : SentimentConfig, optional
        Configuration for sentiment analysis.
    
    Returns
    -------
    tuple
        (textblob_score, vader_score, combined_score)
    
    Examples
    --------
    >>> tb, vader, combined = analyze_sentiment_combined("Great earnings report!")
    >>> print(f"Combined sentiment: {combined:.3f}")
    """
    if config is None:
        config = SentimentConfig()
    
    textblob_score = 0.0
    vader_score = 0.0
    
    if config.use_textblob:
        textblob_score = analyze_sentiment_textblob(text)
    
    if config.use_vader:
        vader_score = analyze_sentiment_vader(text)
    
    if config.combine_scores:
        if config.use_textblob and config.use_vader:
            combined_score = (textblob_score + vader_score) / 2
        elif config.use_textblob:
            combined_score = textblob_score
        else:
            combined_score = vader_score
    else:
        combined_score = vader_score if config.use_vader else textblob_score
    
    return textblob_score, vader_score, combined_score


def classify_sentiment(
    score: float,
    positive_threshold: float = SENTIMENT_POSITIVE_THRESHOLD,
    negative_threshold: float = SENTIMENT_NEGATIVE_THRESHOLD,
) -> str:
    """
    Classify sentiment score into categories.
    
    Parameters
    ----------
    score : float
        Sentiment score.
    positive_threshold : float, default 0.05
        Threshold above which sentiment is considered positive.
    negative_threshold : float, default -0.05
        Threshold below which sentiment is considered negative.
    
    Returns
    -------
    str
        One of 'positive', 'negative', or 'neutral'.
    
    Examples
    --------
    >>> category = classify_sentiment(0.3)
    >>> print(category)  # 'positive'
    """
    if score > positive_threshold:
        return 'positive'
    elif score < negative_threshold:
        return 'negative'
    else:
        return 'neutral'


def analyze_headlines_sentiment(
    df: pd.DataFrame,
    headline_column: str = 'headline',
    config: Optional[SentimentConfig] = None,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Analyze sentiment for all headlines in a dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing headlines.
    headline_column : str, default 'headline'
        Name of the column containing headlines.
    config : SentimentConfig, optional
        Configuration for sentiment analysis.
    show_progress : bool, default True
        If True, show progress during analysis.
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with added sentiment columns:
        - sentiment_textblob
        - sentiment_vader
        - sentiment_combined
        - sentiment_category
    
    Examples
    --------
    >>> df_with_sentiment = analyze_headlines_sentiment(df)
    """
    if config is None:
        config = SentimentConfig()
    
    df = df.copy()
    
    if headline_column not in df.columns:
        raise ValueError(f"Column '{headline_column}' not found in dataframe")
    
    total = len(df)
    
    textblob_scores = []
    vader_scores = []
    combined_scores = []
    
    for i, text in enumerate(df[headline_column]):
        if show_progress and i % 10000 == 0:
            print(f"Processing {i:,}/{total:,} headlines...")
        
        tb, vader, combined = analyze_sentiment_combined(text, config)
        textblob_scores.append(tb)
        vader_scores.append(vader)
        combined_scores.append(combined)
    
    df['sentiment_textblob'] = textblob_scores
    df['sentiment_vader'] = vader_scores
    df['sentiment_combined'] = combined_scores
    df['sentiment_category'] = df['sentiment_combined'].apply(
        lambda x: classify_sentiment(
            x,
            config.positive_threshold,
            config.negative_threshold,
        )
    )
    
    if show_progress:
        print(f"Completed sentiment analysis for {total:,} headlines")
        print(f"Distribution: {df['sentiment_category'].value_counts().to_dict()}")
    
    return df
