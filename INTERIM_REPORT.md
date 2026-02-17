# Interim Report: Predicting Price Moves with News Sentiment

**Project:** Financial News Sentiment Analysis and Stock Price Correlation  
**Challenge:** Week 1 - Stock Challenge (Enhanced in Week 12)  
**Date Started:** November 2024  
**Last Updated:** February 17, 2026  
**Status:** ✅ Week 12 Improvements Completed

---

## Week 12 Enhancement Summary

### Improvements Completed

| Category | Improvement | Status |
|----------|-------------|--------|
| Code Quality | Refactored to modular `src/` structure with type hints | ✅ Complete |
| Code Quality | Created dataclasses for configuration objects | ✅ Complete |
| Testing | Added 35 unit tests with pytest | ✅ Complete |
| CI/CD | Enhanced GitHub Actions with multi-Python testing | ✅ Complete |
| Visualization | Built interactive Streamlit dashboard | ✅ Complete |
| Documentation | Professional README with all required sections | ✅ Complete |
| Documentation | Updated reports for Week 12 submission | ✅ Complete |

### New Project Structure

```
src/
├── config.py           # Dataclasses and constants
├── data/
│   ├── loader.py       # Data loading with type hints
│   └── preprocessor.py # Preprocessing functions
├── analysis/
│   ├── sentiment.py    # TextBlob and VADER sentiment
│   ├── technical.py    # RSI, MACD, SMA, EMA, etc.
│   └── statistics.py   # Gini coefficient, correlations
└── visualization/
    └── plotting.py     # Plotting utilities
```

### Test Results

```
============================= 35 passed in 13.91s ==============================
```

### Key Files Added

- `app/dashboard.py` - Streamlit interactive dashboard
- `tests/test_config.py` - Configuration tests (10 tests)
- `tests/test_analysis.py` - Analysis function tests (25 tests)
- `GAP_ANALYSIS.md` - Week 12 improvement plan
- `pyproject.toml` - Modern Python project configuration
- `.flake8` - Linting configuration

---

---

## Executive Summary

This report documents the progress of analyzing financial news sentiment and its correlation with stock market movements. The project aims to enhance predictive analytics capabilities for Nova Financial Solutions by establishing statistical relationships between news sentiment and stock price fluctuations.

**Current Status:** ✅ **All Week 1 tasks completed successfully!** 

- **Task 1 EDA:** Comprehensive exploratory data analysis of 1.4M+ headlines across 7 structured notebooks with 22 visualizations
- **Task 2 Quantitative Analysis:** Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR) and financial metrics calculated for 6 stocks with 5 visualizations
- **Task 3 Correlation Analysis:** Sentiment analysis performed on 55,230 headlines using TextBlob and VADER, correlation analysis completed with 4 visualizations, key findings and limitations documented

**Next:** Final report preparation and Week 1 submission.

---

## Project Overview

### Business Objective

Nova Financial Solutions aims to enhance its predictive analytics capabilities to significantly boost financial forecasting accuracy and operational efficiency through advanced data analysis. The primary objectives are:

1. **Sentiment Analysis:** Perform sentiment analysis on headline text to quantify the tone and sentiment expressed in financial news using NLP techniques.

2. **Correlation Analysis:** Establish statistical correlations between news sentiment and corresponding stock price movements, tracking price changes around publication dates.

### Dataset Overview

**Financial News and Stock Price Integration Dataset (FNSPID)**

The dataset structure includes:
- **headline:** Article release headline (title of news article)
- **url:** Direct link to the full news article
- **publisher:** Author/creator of article
- **date:** Publication date and time (UTC-4 timezone)
- **stock:** Stock ticker symbol (e.g., AAPL for Apple)

### Key Dates

- **Challenge Introduction:** 10:30 AM UTC, Wednesday, 19 Nov 2025
- **Interim Submission:** 8:00 PM UTC, Sunday, 23 Nov 2025 ⏰
- **Final Submission:** 8:00 PM UTC, Tuesday, 25 Nov 2025

---

## Progress Tracking

### Task 1: Git and GitHub Setup & EDA

**Status:** ✅ Completed  
**Branch:** `task-1` (merged to development)  
**Last Updated:** December 2024

#### Completed Items

- [x] Created GitHub repository
- [x] Set up project structure with required folders
- [x] Created virtual environment (`.venv`)
- [x] Added dependencies to `requirements.txt`
- [x] Initial commit to main branch
- [x] Created `task-1` branch
- [x] Performed initial data loading and exploration
- [x] Created data loading and preprocessing notebook (`01_Data_Loading_and_Setup.ipynb`)
- [x] Developed utility functions module (`utils.py`) with reusable functions
- [x] Created notebook structure documentation (`NOTEBOOK_STRUCTURE.md`)
- [x] Updated notebooks README with usage instructions
- [x] Started EDA notebook (`task1_EDA.ipynb`) with headline length analysis
- [x] Created comprehensive descriptive statistics notebook (`02_Descriptive_Statistics.ipynb`)
- [x] Generated visualization outputs for descriptive statistics
- [x] Organized visualization files in `notebooks/figures/` directory
- [x] Created text analysis notebook (`03_Text_Analysis.ipynb`) with NLP and topic modeling
- [x] Generated visualization outputs for text analysis
- [x] Created time series analysis notebook (`04_Time_Series_Analysis.ipynb`) with temporal pattern analysis
- [x] Generated visualization outputs for time series analysis
- [x] Created publisher analysis notebook (`05_Publisher_Analysis.ipynb`) with publisher deep dive
- [x] Generated visualization outputs for publisher analysis
- [x] Created additional analysis notebook (`06_Additional_Analysis.ipynb`) with supplementary analyses
- [x] Created EDA summary notebook (`00_EDA_Summary.ipynb`) with executive summary
- [x] Generated visualization outputs for additional analysis and summary
- [ ] Set up CI/CD workflows

#### Descriptive Statistics

**Headline Length Analysis:**
- [x] Calculated basic statistics (mean, median, std dev, skewness, kurtosis)
- [x] Created visualizations (histograms, box plots, violin plots)
- [x] Performed outlier detection using IQR method
- [x] Analyzed variation by publisher and stock
- **Findings:** 
  - Dataset contains 1,407,328 headlines
  - Mean headline length: 73.1 characters
  - Median headline length: 64.0 characters
  - Typical headline range: 47-87 characters (25th-75th percentile)
  - Mean word count: 11.4 words, median: 10 words
  - 77,415 headlines (5.50%) are outliers (>147 characters)
  - Headline length varies significantly by publisher (range: 35.3-228.2 characters average)
  - Shortest headline: 3 characters (e.g., "SPY", "SRS")
  - Longest headline: 512 characters
  - **Visualization:** `notebooks/figures/headline_length_analysis.png` - Distribution and outlier analysis

**Publisher Activity:**
- [x] Counted articles per publisher
- [x] Identified most active publishers
- [x] Analyzed long-tail distribution
- [x] Created visualizations (bar charts, cumulative distribution, Pareto chart)
- **Findings:** 
  - Total unique publishers: [To be calculated from notebook output]
  - Top 20 publishers account for significant portion of articles
  - Long-tail distribution observed (few publishers with many articles, many with few)
  - **Visualization:** `notebooks/figures/publisher_activity.png` - Top 20 publishers and cumulative distribution
  - **Visualization:** `notebooks/figures/publisher_distribution.png` - Long-tail and Pareto analysis

**Publication Date Trends:**
- [x] Analyzed publication frequency over time
- [x] Identified yearly, monthly, and daily patterns
- [x] Analyzed day-of-week patterns
- [x] Detected publication spikes (>2 standard deviations)
- [x] Created time series visualizations
- **Findings:** 
  - Date range: 2011-04-27 to 2020-06-11 (for valid dates)
  - Temporal patterns show variations by year, month, and day of week
  - Publication spikes identified for days with unusually high article counts
  - **Visualization:** `notebooks/figures/publication_trends.png` - Temporal patterns and trends

#### Text Analysis (Topic Modeling)

- [x] Extracted common keywords/phrases
- [x] Analyzed bigrams (two-word phrases)
- [x] Performed topic modeling (LDA and NMF)
- [x] Identified significant events (10 event types: FDA approval, price target, earnings, etc.)
- [x] Created visualizations for keywords, events, and topics
- **Key Topics Identified:** 
  - 10 topics extracted using both LDA and NMF methods
  - Topics cover various financial themes (earnings, analyst ratings, market movements, etc.)
  - **Visualization:** `notebooks/figures/top_keywords.png` - Top 20 keywords and top 10 keywords
  - **Visualization:** `notebooks/figures/top_bigrams.png` - Top 10 two-word phrases
  - **Visualization:** `notebooks/figures/event_frequencies.png` - Event type frequency and distribution
  - **Visualization:** `notebooks/figures/lda_topics.png` - LDA topic modeling (10 topics)
  - **Visualization:** `notebooks/figures/nmf_topics.png` - NMF topic modeling (10 topics)
- **Event Detection Results:**
  - 10 event types detected using regex pattern matching
  - Event detection columns added to dataframe for downstream analysis
  - Most common events: [To be updated from notebook output]

#### Time Series Analysis

- [x] Analyzed publication frequency over time (hourly, daily, weekly, monthly)
- [x] Identified publication spikes (2 standard deviations above mean)
- [x] Analyzed publishing times (hourly patterns, day of week patterns)
- [x] Created time-of-day heatmap (hour vs day of week)
- [x] Analyzed yearly publication patterns
- [x] Created visualizations for all temporal analyses
- **Findings:** 
  - Publication frequency shows clear patterns across different time scales
  - Spike detection identifies days with unusually high article counts (>2 std dev above mean)
  - Hourly patterns reveal peak publication times during business hours
  - Day-of-week patterns show differences in publication activity
  - Heatmap visualization reveals publication activity patterns by hour and day
  - Yearly trends show variations in publication volume over time
  - **Visualization:** `notebooks/figures/publication_frequency_over_time.png` - 4-panel view of daily, monthly, weekly, and hourly frequencies
  - **Visualization:** `notebooks/figures/publication_spikes.png` - Spike detection with threshold and distribution analysis
  - **Visualization:** `notebooks/figures/publishing_time_patterns.png` - Day of week and hour of day patterns
  - **Visualization:** `notebooks/figures/time_of_day_heatmap.png` - Heatmap showing publication activity by hour and day of week
  - **Visualization:** `notebooks/figures/yearly_publication_patterns.png` - Yearly trends and patterns

#### Publisher Analysis

- [x] Identified top contributing publishers
- [x] Analyzed publisher statistics, rankings, and articles per day
- [x] Analyzed coverage diversity (unique stocks per publisher)
- [x] Analyzed differences in news types by publisher (event distribution)
- [x] Identified publisher specialization by event type
- [x] Extracted unique domains from email addresses and URLs
- [x] Created visualizations for publisher analysis
- **Findings:** 
  - Top publishers identified with comprehensive statistics
  - Publisher specialization patterns identified for different event types
  - Coverage diversity analysis shows variation in stock coverage across publishers
  - Domain analysis reveals organizational patterns in publisher data
  - **Visualization:** `notebooks/figures/top_publishers_analysis.png` - 4-panel publisher analysis (articles, articles/day, coverage diversity, distribution)
  - **Visualization:** `notebooks/figures/publisher_event_distribution.png` - Event distribution heatmap by publisher (if events available)
  - **Visualization:** `notebooks/figures/publisher_specialization.png` - Dominant event types per publisher (if events available)
  - **Visualization:** `notebooks/figures/domain_analysis.png` - Email/URL domain analysis

#### Git Activity

**Commits Made:**
- Initial project setup
- Add data loading, preprocessing utilities, and initial EDA analysis
  - Created 01_Data_Loading_and_Setup.ipynb for data loading and preprocessing
  - Added utils.py with reusable functions for data quality checks, cleaning, and preprocessing
  - Created task1_EDA.ipynb with headline length analysis
  - Added NOTEBOOK_STRUCTURE.md documenting notebook organization
  - Updated notebooks/README.md with usage instructions
- Add descriptive statistics notebook and visualization outputs
  - Created 02_Descriptive_Statistics.ipynb with comprehensive EDA analysis
    * Headline length analysis (character/word counts, distributions, outliers)
    * Publisher activity analysis (top publishers, long-tail distribution)
    * Publication date trends (yearly, monthly, daily patterns, spike detection)
  - Added 4 visualization PNG files to notebooks/figures/
    * headline_length_analysis.png - Distribution and outlier analysis
    * publication_trends.png - Temporal patterns and trends
    * publisher_activity.png - Top publishers and cumulative distribution
    * publisher_distribution.png - Long-tail and Pareto analysis
  - Updated .gitignore with visualization handling guidelines
  - Removed obsolete task1_EDA.ipynb (replaced by structured notebook approach)
- Add text analysis notebook with NLP and topic modeling
  - Created 03_Text_Analysis.ipynb with comprehensive NLP analysis
    * Keyword and phrase extraction (top 50 keywords, top 20 bigrams)
    * Significant event detection (10 event types using regex patterns)
    * Topic modeling using LDA and NMF (10 topics each, 50K sample)
  - Added 5 visualization PNG files to notebooks/figures/
    * top_keywords.png - Top 20 keywords and top 10 keywords analysis
    * top_bigrams.png - Top 10 two-word phrases (bigrams)
    * event_frequencies.png - Event type frequency (bar chart and pie chart)
    * lda_topics.png - LDA topic modeling visualization (10 topics)
    * nmf_topics.png - NMF topic modeling visualization (10 topics)
  - Fixed NLTK punkt_tab download compatibility for newer NLTK versions
  - Fixed NMF alpha parameter compatibility for newer scikit-learn versions
- Add time series analysis notebook with temporal pattern analysis
  - Created 04_Time_Series_Analysis.ipynb with comprehensive temporal analysis
    * Publication frequency over time (hourly, daily, weekly, monthly trends)
    * Publication spike detection (2 standard deviations above mean)
    * Publishing time analysis (hour of day, day of week patterns)
    * Time-of-day heatmap (hour vs day of week)
    * Yearly publication patterns
  - Added 5 visualization PNG files to notebooks/figures/
    * publication_frequency_over_time.png - 4-panel view of all time scales
    * publication_spikes.png - Spike detection with threshold visualization
    * publishing_time_patterns.png - Day of week and hour patterns
    * time_of_day_heatmap.png - Heatmap showing activity by hour and day
    * yearly_publication_patterns.png - Yearly trends and patterns
- Add publisher analysis, additional analysis, and EDA summary notebooks
  - Created 05_Publisher_Analysis.ipynb with comprehensive publisher analysis
    * Top contributing publishers (statistics, rankings, articles per day, coverage diversity)
    * News type differences by publisher (event distribution, specialization analysis)
    * Email/URL domain analysis (domain extraction and organizational patterns)
  - Created 06_Additional_Analysis.ipynb with supplementary analyses
    * Stock-specific analysis (coverage, headline length, publication patterns by stock)
    * Publisher-stock relationships (coverage matrix, specialization analysis)
    * Data quality checks (missing values, duplicates, anomalies)
    * Cross-analysis insights (stock-event, publisher-stock-event relationships)
  - Created 00_EDA_Summary.ipynb with executive summary
    * High-level dataset overview and key statistics
    * Consolidated key insights from all analyses (placeholders)
    * Summary visualizations dashboard
    * Recommendations for next steps and analysis
  - Added 4 visualization PNG files to notebooks/figures/
    * top_publishers_analysis.png - 4-panel publisher analysis
    * domain_analysis.png - Email/URL domain analysis
    * stock_specific_analysis.png - 4-panel stock-specific analysis
    * eda_summary_dashboard.png - Executive summary dashboard
  - Fixed email extraction regex to use capture groups for str.extract() compatibility
- Add quantitative analysis notebook with TA-Lib and financial metrics
  - Created 07_Quantitative_Analysis.ipynb with comprehensive quantitative analysis
    * Stock price data loading and preparation for 6 stocks (AAPL, AMZN, GOOG, META, MSFT, NVDA)
    * Technical indicators calculation (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
    * Financial metrics calculation (returns, volatility, Sharpe ratio, max drawdown)
    * Trading signal analysis (RSI overbought/oversold, MACD crossovers)
  - Added 5 visualization PNG files to notebooks/figures/
    * stock_prices_with_ma.png - Price charts with moving averages
    * rsi_analysis.png - RSI indicator charts
    * macd_analysis.png - MACD indicator charts
    * returns_volatility_analysis.png - Returns and volatility comparison
    * AAPL_comprehensive_dashboard.png - Comprehensive technical analysis dashboard
  - Updated requirements.txt with pynance dependency
  - Implemented graceful fallback for missing libraries (TA-Lib, PyNance)

**Branches:**
- `main` - Main development branch
- `task-1` - Completed EDA work
- `task-2` - Active development branch for quantitative analysis

---

### Task 2: Quantitative Analysis using PyNance and TA-Lib

**Status:** ✅ Completed  
**Branch:** `task-2` (merged to development)  
**Last Updated:** December 2024

#### Completed Items

- [x] Created `task-2` branch
- [x] Created quantitative analysis notebook (`07_Quantitative_Analysis.ipynb`)
- [x] Loaded stock price data for all 6 stocks (AAPL, AMZN, GOOG, META, MSFT, NVDA)
- [x] Prepared data (Open, High, Low, Close, Volume)
- [x] Calculated technical indicators with TA-Lib (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
- [x] Calculated financial metrics (returns, volatility, Sharpe ratio, max drawdown)
- [x] Created visualizations for technical indicators and financial metrics
- [ ] Applied PyNance for financial metrics (fallback to standard calculations implemented)

#### Technical Indicators

**Moving Averages:**
- [x] Simple Moving Average (SMA) - Calculated for 20, 50, and 200-day periods
- [x] Exponential Moving Average (EMA) - Calculated for 12 and 26-day periods
- **Findings:** 
  - Moving averages provide trend identification across short-term, medium-term, and long-term timeframes
  - Price relative to moving averages indicates trend direction and potential support/resistance levels
  - **Visualization:** `notebooks/figures/stock_prices_with_ma.png` - Price charts with moving averages for all stocks

**RSI (Relative Strength Index):**
- [x] Calculated RSI values (14-period)
- [x] Analyzed overbought/oversold conditions (>70 overbought, <30 oversold)
- **Findings:** 
  - RSI identifies potential reversal points when stocks are overbought or oversold
  - Current RSI values indicate momentum conditions for each stock
  - **Visualization:** `notebooks/figures/rsi_analysis.png` - RSI charts with overbought/oversold zones

**MACD (Moving Average Convergence Divergence):**
- [x] Calculated MACD line, signal line, and histogram (12, 26, 9 parameters)
- [x] Identified buy/sell signals (bullish and bearish crossovers)
- **Findings:** 
  - MACD crossovers identify trend changes and potential entry/exit points
  - Histogram shows momentum strength
  - **Visualization:** `notebooks/figures/macd_analysis.png` - MACD charts with signal lines and histograms

**Additional Indicators:**
- [x] Bollinger Bands - Price volatility bands (20-period, 2 standard deviations)
- [x] ATR (Average True Range) - Volatility measurement (14-period)

#### Financial Metrics

- [x] Calculated daily and cumulative returns
- [x] Calculated volatility (30-day rolling, annualized)
- [x] Calculated Sharpe Ratio (risk-adjusted returns)
- [x] Calculated Max Drawdown (downside risk)
- [x] Calculated price changes and spreads
- **Metrics Calculated:** 
  - Daily Returns, Cumulative Returns
  - Volatility (30-day rolling, annualized)
  - Sharpe Ratio (annualized, assuming risk-free rate of 0)
  - Max Drawdown
  - Price Change, Price Change Percentage
  - High-Low Spread, High-Low Spread Percentage
- **Findings:** 
  - Returns and volatility metrics provide risk-return profiles for each stock
  - Sharpe ratios enable comparison of risk-adjusted performance across stocks
  - Max drawdowns identify worst-case scenarios for each stock
  - **Visualization:** `notebooks/figures/returns_volatility_analysis.png` - Cumulative returns and volatility comparison
- **Note:** PyNance library not available; standard financial calculations implemented as fallback

#### Visualizations

- [x] Stock price charts with moving averages
- [x] RSI indicator charts with overbought/oversold zones
- [x] MACD indicator charts with signal lines and histograms
- [x] Returns and volatility comparison charts
- [x] Comprehensive technical analysis dashboard
- **Charts Created:** 
  - `stock_prices_with_ma.png` - Stock prices with moving averages for all 6 stocks
  - `rsi_analysis.png` - RSI charts showing overbought/oversold conditions
  - `macd_analysis.png` - MACD charts with signal lines and histograms
  - `returns_volatility_analysis.png` - Cumulative returns and volatility comparison
  - `AAPL_comprehensive_dashboard.png` - 4-panel comprehensive dashboard (price with indicators, RSI, MACD, volume)

---

### Task 3: Correlation between News and Stock Movement

**Status:** ✅ Completed  
**Branch:** `task-3`  
**Last Updated:** December 2024

#### Completed Items

- [x] Created `task-3` branch
- [x] Created correlation analysis notebook (`08_Correlation_Analysis.ipynb`)
- [x] Aligned news and stock datasets by date (normalized timestamps, matched to trading days)
- [x] Performed sentiment analysis on headlines using TextBlob and VADER
- [x] Calculated daily stock returns for all 6 stocks
- [x] Aggregated daily sentiment scores
- [x] Performed correlation analysis (Pearson correlation, statistical significance testing)
- [x] Performed lagged correlation analysis
- [x] Created comprehensive visualizations
- [x] Documented key findings, challenges, and recommendations

#### Data Preparation

**Date Alignment:**
- [x] Normalized timestamps and extracted date-only values
- [x] Matched news items to trading days (98.65% of valid news dates aligned)
- [x] Identified trading days from stock data (3,774 unique trading days)
- **Challenges Encountered:** Extremely limited data overlap (0.05-0.13% of trading days have matching news sentiment data)

#### Sentiment Analysis

**Tools Used:**
- [x] NLTK (for text preprocessing)
- [x] TextBlob (polarity scores)
- [x] VADER Sentiment (compound scores, optimized for financial text)

**Sentiment Scores:**
- [x] Assigned sentiment scores to 55,230 headlines
- [x] Created combined sentiment score (average of TextBlob and VADER)
- [x] Classified sentiment as positive, negative, or neutral
- **Findings:** 
  - Distribution: 52.13% neutral, 28.66% positive, 19.20% negative
  - Mean combined sentiment: 0.0525 (slightly positive)
  - Most positive stocks: AMZN (0.1902), AAPL (0.1768), NVDA (0.1805)
  - Least positive: GOOG (0.0174)
  - **Visualization:** `notebooks/figures/sentiment_analysis.png` - Sentiment distribution and comparison charts

#### Stock Movement Calculation

**Daily Returns:**
- [x] Calculated percentage change in closing prices for all 6 stocks
- [x] Analyzed return distribution and statistics
- **Findings:** 
  - All stocks show positive mean daily returns (0.09% to 0.19%)
  - NVDA has highest volatility (2.89% std dev) and highest mean return (0.19%)
  - All stocks show roughly balanced positive/negative days (52-53% positive)
  - **Visualization:** `notebooks/figures/stock_returns_distribution.png` - Returns distribution for all stocks

#### Correlation Analysis

**Aggregation:**
- [x] Computed average daily sentiment scores (43,466 date-stock combinations)
- [x] Handled multiple articles per day (average 1.27 articles per day-stock)
- [x] Merged sentiment with stock returns by date and stock

**Correlation Results:**
- [x] Calculated Pearson correlation coefficient for each stock
- [x] Performed statistical significance testing (p-values)
- [x] Calculated R-squared values
- [x] Performed lagged correlation analysis (sentiment today → returns tomorrow)
- **Correlation Values:** 
  - AAPL: r = -1.0000 (2 observations, not significant)
  - AMZN: r = -1.0000 (2 observations, not significant)
  - GOOG: r = -0.2153 (5 observations, not significant, p = 0.73)
  - NVDA: r = 0.4400 (4 observations, not significant, p = 0.56)
  - META & MSFT: No data overlap
  - Average correlation: -0.4438 (unreliable due to small samples)
- **Statistical Significance:** No significant correlations found (all p-values > 0.05)
- **Key Limitation:** Extremely limited data overlap (0.05-0.13% coverage) prevents robust correlation analysis
- **Lagged Correlation:** No predictive power detected (GOOG: r = -0.0439, NVDA: r = 0.3051, both not significant)
- **Visualizations:** 
  - `notebooks/figures/sentiment_returns_correlation.png` - Scatter plots of sentiment vs returns
  - `notebooks/figures/correlation_summary.png` - Correlation coefficients and R-squared summary

---

## Key Findings & Insights

### Preliminary Insights

1. **Dataset Scale:** The dataset contains over 1.4 million financial news headlines, providing a substantial foundation for analysis.

2. **Headline Characteristics:** 
   - Headlines follow a relatively normal distribution with a median length of 64 characters (10 words)
   - Significant variation exists between publishers, with average headline lengths ranging from 35.3 to 228.2 characters
   - Approximately 5.5% of headlines are outliers, suggesting diverse content types
   - **Visualization Reference:** See `notebooks/figures/headline_length_analysis.png` for detailed distribution analysis

3. **Publisher Distribution:**
   - Long-tail distribution observed: few publishers dominate with many articles, while many publishers have few articles
   - Top publishers account for significant portion of total articles
   - Clear concentration of publishing activity among top contributors
   - **Visualization Reference:** See `notebooks/figures/publisher_activity.png` and `notebooks/figures/publisher_distribution.png` for publisher analysis

4. **Temporal Patterns:**
   - Publication activity shows clear temporal trends across years, months, and days of week
   - Publication spikes identified for days with unusually high article counts (>2 standard deviations)
   - Day-of-week patterns reveal when most news is published
   - **Visualization Reference:** See `notebooks/figures/publication_trends.png` for temporal analysis

5. **Data Quality:** 
   - No missing values in the dataset
   - High duplicate rate: 39.90% duplicate headlines, 37.23% duplicate URLs
   - Date validation issues: 96.02% of dates are invalid (converted to NaT), requiring careful handling

6. **Text Analysis Insights:**
   - Top keywords identified through frequency analysis
   - 10 significant financial event types detected using pattern matching
   - Topic modeling reveals main themes in financial news (earnings, analyst ratings, market movements, etc.)
   - Both LDA and NMF methods provide complementary topic perspectives
   - **Visualization References:** See `notebooks/figures/top_keywords.png`, `notebooks/figures/top_bigrams.png`, `notebooks/figures/event_frequencies.png`, `notebooks/figures/lda_topics.png`, and `notebooks/figures/nmf_topics.png` for text analysis results

7. **Time Series Analysis Insights:**
   - Publication frequency shows clear temporal patterns across hourly, daily, weekly, and monthly scales
   - Spike detection identifies days with unusually high publication activity (>2 standard deviations)
   - Hourly patterns reveal peak publication times during business hours
   - Day-of-week analysis shows differences in publication activity across weekdays
   - Heatmap visualization reveals publication activity patterns by hour and day of week
   - Yearly trends show variations in publication volume over the dataset's time range
   - **Visualization References:** See `notebooks/figures/publication_frequency_over_time.png`, `notebooks/figures/publication_spikes.png`, `notebooks/figures/publishing_time_patterns.png`, `notebooks/figures/time_of_day_heatmap.png`, and `notebooks/figures/yearly_publication_patterns.png` for temporal analysis results

8. **Publisher Analysis Insights:**
   - Top publishers identified with comprehensive statistics (articles, articles/day, coverage diversity)
   - Publisher specialization patterns identified for different event types
   - Coverage diversity analysis shows variation in stock coverage across publishers
   - Domain analysis reveals organizational patterns in publisher data
   - **Visualization References:** See `notebooks/figures/top_publishers_analysis.png`, `notebooks/figures/domain_analysis.png`, and related publisher analysis visualizations

9. **Additional Analysis Insights:**
   - Stock-specific patterns reveal differences in coverage, headline length, and publication frequency
   - Publisher-stock relationships show coverage matrices and specialization patterns
   - Cross-analysis insights combine stocks, publishers, and events to identify patterns
   - Data quality checks identify potential issues for downstream analysis
   - **Visualization References:** See `notebooks/figures/stock_specific_analysis.png` and related cross-analysis visualizations

10. **Infrastructure:** Successfully established a modular notebook structure with reusable utility functions, enabling efficient and organized analysis workflow. All EDA notebooks completed and ready for Task 2.

11. **Quantitative Analysis Insights:**
    - Technical indicators (SMA, EMA, RSI, MACD) successfully calculated for all 6 stocks
    - Financial metrics (returns, volatility, Sharpe ratio, max drawdown) provide risk-return profiles
    - Trading signals identified through RSI overbought/oversold conditions and MACD crossovers
    - Comparative analysis reveals differences in performance and risk across stocks
    - **Visualization References:** See `notebooks/figures/stock_prices_with_ma.png`, `notebooks/figures/rsi_analysis.png`, `notebooks/figures/macd_analysis.png`, `notebooks/figures/returns_volatility_analysis.png`, and `notebooks/figures/AAPL_comprehensive_dashboard.png` for quantitative analysis results

12. **Correlation Analysis Insights:**
    - Sentiment analysis performed on 55,230 headlines using TextBlob and VADER
    - Sentiment distribution: 52% neutral, 29% positive, 19% negative (slightly positive bias)
    - Stock returns calculated for all 6 stocks (positive mean returns: 0.09-0.19%)
    - Critical limitation identified: Extremely limited data overlap (0.05-0.13% of trading days have matching news)
    - No statistically significant correlations found (all p-values > 0.05, small sample sizes)
    - Date alignment issues prevent robust correlation analysis
    - Recommendations provided for improving data alignment and alternative analysis approaches
    - **Visualization References:** See `notebooks/figures/sentiment_analysis.png`, `notebooks/figures/stock_returns_distribution.png`, `notebooks/figures/sentiment_returns_correlation.png`, and `notebooks/figures/correlation_summary.png` for correlation analysis results

### Challenges Encountered

1. **Date Parsing Issues:** The majority of dates (96.02%) in the dataset are invalid or improperly formatted. This required implementing robust date handling in the preprocessing pipeline to convert dates to datetime format and handle invalid entries gracefully.

2. **Large Dataset Size:** With over 1.4 million rows, initial data loading and processing required optimization. Implemented chunking strategies and efficient data type conversions to manage memory usage. For topic modeling, used sampling (50,000 headlines) to make computation feasible.

3. **Duplicate Content:** High percentage of duplicate headlines and URLs suggests potential data quality issues or content syndication. This will need to be addressed in downstream analysis to avoid bias.

4. **NLTK Compatibility:** Newer versions of NLTK require `punkt_tab` instead of `punkt` for tokenization. Resolved by updating download code to handle both versions with proper fallback mechanism.

5. **Scikit-learn API Changes:** NMF class in newer scikit-learn versions replaced `alpha` parameter with `alpha_W` and `alpha_H`. Resolved by implementing version-compatible code with try-except fallback to support both old and new API versions.

6. **Pandas str.extract() Requirements:** The `str.extract()` method requires regex patterns with capture groups (parentheses). Fixed email extraction by adding capture groups to the regex pattern.

7. **TA-Lib Installation:** TA-Lib requires C library installation before Python package installation. Provided clear error messages and fallback handling in notebook.

8. **PyNance Library Availability:** PyNance library may not be available as a standard package. Implemented fallback to standard financial calculations using pandas/numpy for all required metrics.

9. **Date Alignment in Correlation Analysis:** Extremely limited data overlap between news dates (2011-2020) and stock trading days (2009-2023) resulted in only 0.05-0.13% coverage. This prevented robust correlation analysis due to insufficient sample sizes (2-5 observations per stock). Identified as a critical limitation requiring data investigation and alternative approaches.

### Lessons Learned

1. **Modular Design:** Creating reusable utility functions (`utils.py`) early in the project significantly improved code organization and reusability across multiple notebooks.

2. **Data Quality First:** Performing comprehensive data quality checks before analysis revealed critical issues (date formatting, duplicates) that would have impacted downstream analysis if not addressed early.

3. **Incremental Development:** Breaking down the EDA into focused notebooks (data loading, descriptive stats, text analysis, etc.) allows for parallel development and easier debugging.

4. **Library Version Compatibility:** Different versions of libraries (NLTK, scikit-learn, pandas) may have API changes. Implementing version-compatible code with fallbacks ensures notebooks work across different environments.

5. **Complete EDA Workflow:** Successfully completed all planned EDA notebooks (01-06 plus summary), creating a comprehensive analysis framework that can be reused and extended for future projects.

6. **Library Availability Handling:** Implementing graceful fallbacks for optional libraries (TA-Lib, PyNance) ensures notebooks can run even if some dependencies are missing, with clear error messages guiding users.

7. **Data Alignment Challenges:** Date alignment between different data sources is critical for correlation analysis. The mismatch between news data dates and stock trading days highlighted the importance of thorough data investigation before analysis. Alternative approaches (weekly/monthly aggregation) may be necessary when daily alignment is not feasible.

8. **Sentiment Analysis Tools:** Using multiple sentiment analysis tools (TextBlob and VADER) provides complementary perspectives. VADER is optimized for social media and financial text, while TextBlob provides more general sentiment analysis. Combining both tools gives a more robust sentiment score.

---

## Next Steps

### Immediate Actions

1. [x] Complete descriptive statistics analysis (headline length, publisher activity, publication trends)
2. [x] Create visualizations for descriptive statistics
3. [x] Organize visualization files in dedicated directory
4. [x] Complete text analysis (keyword extraction, event detection, topic modeling)
5. [x] Create visualizations for text analysis
6. [x] Complete time series analysis (publication frequency, spike detection, publishing time patterns)
7. [x] Create visualizations for time series analysis
8. [x] Complete publisher analysis (top publishers, specialization, domain analysis)
9. [x] Create visualizations for publisher analysis
10. [x] Complete additional analysis (stock-specific, publisher-stock relationships, cross-analysis)
11. [x] Create visualizations for additional analysis
12. [x] Create EDA summary notebook with executive summary
13. [x] Document key insights and findings from all analyses
14. [ ] Prepare Task 1 summary for merge to main
15. [x] Begin Task 2 data preparation (stock price data loading)
16. [x] Calculate technical indicators with TA-Lib
17. [x] Calculate financial metrics
18. [x] Create visualizations for quantitative analysis
19. [x] Complete Task 3: Correlation between News and Stock Movement
20. [x] Perform sentiment analysis on headlines
21. [x] Calculate correlations between sentiment and stock returns
22. [x] Document findings, challenges, and recommendations
23. [x] Update interim report with Task 3 completion
24. [ ] Prepare final report for Week 1 submission

### Upcoming Tasks

- [ ] Merge Task 1 branch to main via PR
- [x] Start Task 2: Technical indicators analysis
- [ ] Complete Task 2: Finalize quantitative analysis
- [ ] Begin Task 3: Sentiment and correlation analysis
- [ ] Prepare final report

---

## Technical Details

### Environment Setup

- **Python Version:** [To be updated]
- **Virtual Environment:** `.venv`
- **Key Dependencies:** See `requirements.txt`

### Data Sources

- **News Data:** `data/raw_analyst_ratings.csv` (1,407,328 rows)
  - Contains: headline, url, publisher, date, stock ticker
  - Date range: 2011-04-27 to 2020-06-11 (for valid dates)
  - Processed data saved to: `data/processed/df_processed.pkl`
- **Stock Data:** `data/Data/Data/` directory (AAPL, AMZN, GOOG, META, MSFT, NVDA CSV files)

### Tools & Libraries

- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn
- **NLP:** nltk, textblob, vaderSentiment
- **Technical Analysis:** TA-Lib, PyNance
- **Statistical Analysis:** scipy, scikit-learn

---

## References & Resources

[Add references, tutorials, and resources you've used]

1. [Resource 1]
2. [Resource 2]

---

## Appendix

### Code Snippets

[Add important code snippets or functions you've created]

### Visualizations

**Descriptive Statistics Visualizations:**

1. **Headline Length Analysis** (`notebooks/figures/headline_length_analysis.png`)
   - Distribution of headline character lengths (histogram)
   - Box plot showing quartiles and outliers
   - Word count distribution (histogram)
   - Violin plot for word count distribution
   - Shows mean, median, and distribution characteristics

2. **Publisher Activity** (`notebooks/figures/publisher_activity.png`)
   - Top 20 publishers by article count (horizontal bar chart)
   - Cumulative distribution of articles by publisher rank
   - Shows concentration of publishing activity

3. **Publisher Distribution** (`notebooks/figures/publisher_distribution.png`)
   - Distribution of publisher activity (log scale histogram)
   - Pareto chart of top 30 publishers
   - Illustrates long-tail distribution pattern

4. **Publication Trends** (`notebooks/figures/publication_trends.png`)
   - Daily article publication frequency (time series)
   - Articles per month (aggregated bar chart)
   - Articles per day of week (bar chart)
   - Articles per year (bar chart)
   - Shows temporal patterns and trends

**Text Analysis Visualizations:**

5. **Top Keywords** (`notebooks/figures/top_keywords.png`)
   - Top 20 keywords in headlines (horizontal bar chart)
   - Top 10 keywords (vertical bar chart)
   - Shows most frequent terms after stopword removal

6. **Top Bigrams** (`notebooks/figures/top_bigrams.png`)
   - Top 10 two-word phrases (bigrams) in headlines
   - Horizontal bar chart showing phrase frequencies
   - Identifies common financial news phrases

7. **Event Frequencies** (`notebooks/figures/event_frequencies.png`)
   - Frequency of significant events (horizontal bar chart)
   - Distribution of event types (pie chart for top 6 events)
   - Shows prevalence of different financial event types

8. **LDA Topics** (`notebooks/figures/lda_topics.png`)
   - 10 topics identified using Latent Dirichlet Allocation
   - Top 10 words per topic with weights
   - 2x5 grid visualization showing all topics

9. **NMF Topics** (`notebooks/figures/nmf_topics.png`)
   - 10 topics identified using Non-negative Matrix Factorization
   - Top 10 words per topic with weights
   - 2x5 grid visualization showing all topics
   - Alternative topic modeling approach for comparison

**Time Series Analysis Visualizations:**

10. **Publication Frequency Over Time** (`notebooks/figures/publication_frequency_over_time.png`)
    - 4-panel visualization showing publication frequency across different time scales
    - Daily publication frequency (time series line chart)
    - Monthly publication frequency (bar chart)
    - Weekly publication frequency (time series line chart)
    - Hourly publication frequency (bar chart for all days)
    - Provides comprehensive view of temporal publication patterns

11. **Publication Spikes** (`notebooks/figures/publication_spikes.png`)
    - Daily publication frequency with spike threshold line
    - Scatter plot highlighting spike days (red points)
    - Distribution histogram of daily publication counts
    - Shows mean, threshold, and spike identification
    - Identifies days with unusually high publication activity (>2 std dev)

12. **Publishing Time Patterns** (`notebooks/figures/publishing_time_patterns.png`)
    - Articles published by day of week (bar chart with value labels)
    - Articles published by hour of day (bar chart with top 10% labeled)
    - Shows clear patterns in when news is most frequently published
    - Reveals peak publication times during business hours

13. **Time-of-Day Heatmap** (`notebooks/figures/time_of_day_heatmap.png`)
    - Heatmap showing publication activity by hour (x-axis) and day of week (y-axis)
    - Color intensity represents number of articles published
    - Reveals publication activity patterns across the week
    - Identifies peak hours and days for news publication

14. **Yearly Publication Patterns** (`notebooks/figures/yearly_publication_patterns.png`)
    - Total articles published by year (bar chart)
    - Yearly publication trend (line chart with markers)
    - Shows variations in publication volume over time
    - Identifies years with highest and lowest publication activity

**Publisher Analysis Visualizations:**

15. **Top Publishers Analysis** (`notebooks/figures/top_publishers_analysis.png`)
    - 4-panel visualization showing comprehensive publisher analysis
    - Top 20 publishers by article count (horizontal bar chart)
    - Articles per day for top 20 publishers (horizontal bar chart)
    - Coverage diversity (unique stocks) for top 20 publishers (horizontal bar chart)
    - Distribution of articles per publisher (log scale histogram)
    - Provides comprehensive view of publisher characteristics

16. **Publisher Event Distribution** (`notebooks/figures/publisher_event_distribution.png`)
    - Heatmap showing event distribution by publisher (top 15 publishers, top 10 events)
    - Color intensity represents percentage of articles with each event type
    - Reveals publisher specialization patterns
    - Shows which publishers focus on specific event types

17. **Publisher Specialization** (`notebooks/figures/publisher_specialization.png`)
    - Dominant event type for each top publisher (horizontal bar chart)
    - Shows percentage of articles with dominant event type
    - Identifies publishers that specialize in specific financial event types

18. **Domain Analysis** (`notebooks/figures/domain_analysis.png`)
    - Top 20 email/URL domains by article count (horizontal bar chart)
    - Distribution of articles per domain (log scale histogram)
    - Reveals organizational patterns in publisher data
    - Shows concentration of articles across different domains

**Additional Analysis Visualizations:**

19. **Stock-Specific Analysis** (`notebooks/figures/stock_specific_analysis.png`)
    - 4-panel visualization showing stock-specific patterns
    - Articles per stock (bar chart)
    - Mean headline length by stock (bar chart)
    - Publisher diversity by stock (bar chart)
    - Articles per day by stock (bar chart)
    - Provides comprehensive view of stock coverage patterns

20. **Publisher-Stock Relationships** (`notebooks/figures/publisher_stock_relationships.png`)
    - Heatmap showing publisher-stock coverage (top 15 publishers, all stocks)
    - Color intensity represents number of articles
    - Reveals which publishers cover which stocks
    - Identifies publisher-stock specialization patterns

21. **Stock-Event Relationships** (`notebooks/figures/stock_event_relationships.png`)
    - Heatmap showing event distribution by stock (top 5 events)
    - Color intensity represents percentage of articles with each event type
    - Reveals which events are most common for each stock
    - Shows stock-specific event patterns

**EDA Summary Visualizations:**

22. **EDA Summary Dashboard** (`notebooks/figures/eda_summary_dashboard.png`)
    - 4-panel executive summary dashboard
    - Articles per stock (bar chart)
    - Top 10 publishers (horizontal bar chart)
    - Headline length distribution (histogram with mean/median)
    - Publication timeline (yearly trend line chart)
    - Provides high-level overview of entire dataset

**Quantitative Analysis Visualizations:**

23. **Stock Prices with Moving Averages** (`notebooks/figures/stock_prices_with_ma.png`)
    - Price charts for all 6 stocks with multiple moving averages
    - Shows SMA (20, 50, 200) and EMA (12, 26) overlays
    - Identifies trend directions and support/resistance levels
    - Provides comprehensive view of price movements with technical indicators

24. **RSI Analysis** (`notebooks/figures/rsi_analysis.png`)
    - RSI indicator charts for all stocks
    - Overbought (>70) and oversold (<30) zones highlighted
    - Shows momentum conditions and potential reversal points
    - Identifies periods of extreme buying or selling pressure

25. **MACD Analysis** (`notebooks/figures/macd_analysis.png`)
    - MACD charts with signal lines and histograms for all stocks
    - Shows MACD line, signal line, and histogram
    - Identifies bullish and bearish crossovers
    - Reveals trend changes and momentum shifts

26. **Returns and Volatility Analysis** (`notebooks/figures/returns_volatility_analysis.png`)
    - Cumulative returns comparison across all stocks
    - 30-day rolling volatility (annualized) comparison
    - Shows risk-return profiles for each stock
    - Enables comparison of performance and risk levels

27. **AAPL Comprehensive Dashboard** (`notebooks/figures/AAPL_comprehensive_dashboard.png`)
    - 4-panel comprehensive technical analysis dashboard
    - Price with moving averages and Bollinger Bands
    - RSI indicator with overbought/oversold zones
    - MACD with signal line and histogram
    - Volume analysis
    - Provides complete technical analysis view for one stock

All visualizations are saved in high resolution (300 DPI) for documentation and presentation purposes.

---

**Report Maintenance:** This document should be updated regularly as you progress through the tasks. Commit changes with descriptive messages like "Update interim report: Task 1 EDA completed" or "Update interim report: Added correlation findings".

