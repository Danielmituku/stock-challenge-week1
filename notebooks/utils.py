"""
Shared utility functions for EDA notebooks
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data(file_path='../data/raw_analyst_ratings.csv', sample_size=None):
    """
    Load the raw analyst ratings dataset.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    sample_size : int, optional
        If provided, randomly sample this many rows for faster processing
    
    Returns:
    --------
    df : pandas.DataFrame
        Raw dataframe
    """
    print("Loading dataset...")
    
    if sample_size:
        df = pd.read_csv(file_path, nrows=sample_size)
        print(f"Loaded sample of {len(df):,} rows")
    else:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df):,} rows")
    
    print(f"Initial shape: {df.shape}")
    return df


def check_data_quality(df):
    """
    Perform comprehensive data quality checks.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe to check
    
    Returns:
    --------
    dict : Dictionary with quality check results
    """
    print("="*80)
    print("DATA QUALITY CHECKS")
    print("="*80)
    
    quality_report = {}
    
    # Missing values
    print("\n1. MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    
    if len(missing_df) > 0:
        print(missing_df.to_string())
        quality_report['missing_values'] = missing_df.to_dict()
    else:
        print("✓ No missing values found!")
        quality_report['missing_values'] = None
    
    # Duplicates
    print("\n2. DUPLICATE RECORDS:")
    duplicate_rows = df.duplicated().sum()
    duplicate_headlines = df['headline'].duplicated().sum()
    duplicate_urls = df['url'].duplicated().sum()
    
    print(f"  • Duplicate rows: {duplicate_rows:,} ({duplicate_rows/len(df)*100:.2f}%)")
    print(f"  • Duplicate headlines: {duplicate_headlines:,} ({duplicate_headlines/len(df)*100:.2f}%)")
    print(f"  • Duplicate URLs: {duplicate_urls:,} ({duplicate_urls/len(df)*100:.2f}%)")
    
    quality_report['duplicates'] = {
        'rows': duplicate_rows,
        'headlines': duplicate_headlines,
        'urls': duplicate_urls
    }
    
    # Data types
    print("\n3. DATA TYPES:")
    print(df.dtypes.to_string())
    quality_report['dtypes'] = df.dtypes.to_dict()
    
    # Date range check
    if 'date' in df.columns:
        print("\n4. DATE RANGE:")
        try:
            dates = pd.to_datetime(df['date'], errors='coerce')
            valid_dates = dates.notna().sum()
            invalid_dates = dates.isna().sum()
            print(f"  • Valid dates: {valid_dates:,} ({valid_dates/len(df)*100:.2f}%)")
            print(f"  • Invalid dates: {invalid_dates:,} ({invalid_dates/len(df)*100:.2f}%)")
            if valid_dates > 0:
                print(f"  • Date range: {dates.min()} to {dates.max()}")
            quality_report['date_quality'] = {
                'valid': valid_dates,
                'invalid': invalid_dates
            }
        except:
            print("  ⚠ Could not parse dates")
            quality_report['date_quality'] = None
    
    # Outlier detection (for numeric columns)
    print("\n5. OUTLIER DETECTION (IQR Method):")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        outlier_summary = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outliers > 0:
                print(f"  • {col}: {outliers:,} outliers ({outliers/len(df)*100:.2f}%)")
                outlier_summary[col] = {
                    'count': outliers,
                    'percentage': outliers/len(df)*100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        if not outlier_summary:
            print("  ✓ No significant outliers detected in numeric columns")
        quality_report['outliers'] = outlier_summary
    else:
        print("  No numeric columns found for outlier detection")
        quality_report['outliers'] = None
    
    return quality_report


def clean_data(df, remove_duplicates=True, handle_missing='report', fix_dates=True):
    """
    Clean the dataset by handling missing values, duplicates, and data type issues.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe to clean
    remove_duplicates : bool
        If True, remove duplicate rows
    handle_missing : str
        'report' - only report missing values
        'drop' - drop rows with missing values
        'fill' - fill missing values (for numeric: median, for text: 'Unknown')
    fix_dates : bool
        If True, convert date column and handle invalid dates
    
    Returns:
    --------
    df_clean : pandas.DataFrame
        Cleaned dataframe
    """
    df_clean = df.copy()
    original_shape = df_clean.shape
    
    print("="*80)
    print("DATA CLEANING")
    print("="*80)
    
    # Handle dates
    if fix_dates and 'date' in df_clean.columns:
        print("\n1. Converting date column...")
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        invalid_dates = df_clean['date'].isna().sum()
        if invalid_dates > 0:
            print(f"   ⚠ Found {invalid_dates:,} invalid dates (converted to NaT)")
            if handle_missing == 'drop':
                df_clean = df_clean.dropna(subset=['date'])
                print(f"   → Dropped {invalid_dates:,} rows with invalid dates")
    
    # Handle missing values
    if handle_missing != 'report':
        print("\n2. Handling missing values...")
        missing_before = df_clean.isnull().sum().sum()
        
        if handle_missing == 'drop':
            df_clean = df_clean.dropna()
            print(f"   → Dropped rows with missing values")
        elif handle_missing == 'fill':
            for col in df_clean.columns:
                if df_clean[col].isnull().sum() > 0:
                    if df_clean[col].dtype in ['int64', 'float64']:
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    else:
                        df_clean[col].fillna('Unknown', inplace=True)
            print(f"   → Filled missing values")
        
        missing_after = df_clean.isnull().sum().sum()
        print(f"   Missing values: {missing_before:,} → {missing_after:,}")
    
    # Remove duplicates
    if remove_duplicates:
        print("\n3. Removing duplicates...")
        duplicates_before = df_clean.duplicated().sum()
        df_clean = df_clean.drop_duplicates()
        duplicates_removed = duplicates_before
        print(f"   → Removed {duplicates_removed:,} duplicate rows")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"CLEANING SUMMARY:")
    print(f"  Original shape: {original_shape}")
    print(f"  Cleaned shape:  {df_clean.shape}")
    print(f"  Rows removed:   {original_shape[0] - df_clean.shape[0]:,}")
    print(f"  Columns:        {original_shape[1]} → {df_clean.shape[1]}")
    print(f"{'='*80}")
    
    return df_clean


def preprocess_data(df):
    """
    Create derived features and perform preprocessing steps.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned dataframe
    
    Returns:
    --------
    df : pandas.DataFrame
        Dataframe with derived features
    """
    print("\n" + "="*80)
    print("FEATURE ENGINEERING")
    print("="*80)
    
    # Extract temporal features
    if 'date' in df.columns and df['date'].dtype == 'datetime64[ns]':
        print("\n1. Extracting temporal features...")
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['date_only'] = df['date'].dt.date
        print("   ✓ Temporal features created")
    
    # Calculate headline lengths
    if 'headline' in df.columns:
        print("\n2. Calculating headline metrics...")
        df['headline_length'] = df['headline'].str.len()
        df['headline_word_count'] = df['headline'].str.split().str.len()
        print("   ✓ Headline length metrics created")
    
    print(f"\nFinal shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df


def load_and_preprocess_data(file_path='../data/raw_analyst_ratings.csv', 
                             sample_size=None,
                             clean=True,
                             remove_duplicates=True,
                             handle_missing='report'):
    """
    Complete pipeline: Load, check quality, clean, and preprocess data.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    sample_size : int, optional
        If provided, randomly sample this many rows
    clean : bool
        If True, perform data cleaning
    remove_duplicates : bool
        If True, remove duplicate rows
    handle_missing : str
        'report', 'drop', or 'fill'
    
    Returns:
    --------
    df : pandas.DataFrame
        Fully processed dataframe
    quality_report : dict
        Data quality report
    """
    # Load
    df = load_data(file_path, sample_size)
    
    # Check quality
    quality_report = check_data_quality(df)
    
    # Clean
    if clean:
        df = clean_data(df, remove_duplicates=remove_duplicates, 
                       handle_missing=handle_missing, fix_dates=True)
    
    # Preprocess
    df = preprocess_data(df)
    
    return df, quality_report


def save_processed_data(df, file_path='../data/processed/df_processed.pkl'):
    """Save processed dataframe to pickle file"""
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_pickle(file_path)
    print(f"Saved processed data to {file_path}")


def load_processed_data(file_path='../data/processed/df_processed.pkl'):
    """Load processed dataframe from pickle file"""
    df = pd.read_pickle(file_path)
    print(f"Loaded processed data from {file_path}")
    print(f"Shape: {df.shape}")
    return df


def setup_plotting_style():
    """Set up consistent plotting style across notebooks"""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    print("Plotting style configured")


def gini_coefficient(values):
    """
    Calculate Gini coefficient to measure inequality.
    
    Parameters:
    -----------
    values : array-like
        Values to calculate Gini coefficient for
    
    Returns:
    --------
    float : Gini coefficient (0 = perfect equality, 1 = perfect inequality)
    """
    sorted_values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n


def identify_spikes(series, threshold_std=2):
    """
    Identify spikes in a time series.
    
    Parameters:
    -----------
    series : pandas.Series
        Time series data
    threshold_std : float
        Number of standard deviations above mean to consider a spike
    
    Returns:
    --------
    pandas.Series : Spikes identified
    """
    mean = series.mean()
    std = series.std()
    threshold = mean + threshold_std * std
    spikes = series[series > threshold]
    return spikes


def extract_email_domain(publisher):
    """
    Extract email domain from publisher name if it's an email address.
    
    Parameters:
    -----------
    publisher : str
        Publisher name (may be email address)
    
    Returns:
    --------
    str or None : Domain if email found, None otherwise
    """
    import re
    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    match = re.search(email_pattern, str(publisher))
    if match:
        return match.group(1).split('@')[1]
    return None

