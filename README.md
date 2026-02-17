# 📈 Financial News Sentiment Analysis & Stock Price Correlation

[![CI Pipeline](https://github.com/username/stock-challenge-week1/actions/workflows/ci.yml/badge.svg)](https://github.com/username/stock-challenge-week1/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive analysis of financial news sentiment and its correlation with stock price movements. This project combines NLP-based sentiment analysis with technical indicators to explore the relationship between news sentiment and market behavior for major tech stocks.

## 🎯 Business Problem

**Challenge:** Can we predict stock market movements by analyzing the sentiment of financial news?

Financial institutions and investors seek to understand how news sentiment impacts stock prices. This project addresses this challenge by:

1. **Quantifying News Sentiment**: Using NLP techniques (TextBlob, VADER) to analyze 1.4M+ financial headlines
2. **Technical Analysis**: Calculating key indicators (RSI, MACD, Moving Averages) for informed trading decisions
3. **Correlation Analysis**: Establishing statistical relationships between sentiment and price movements

## 💡 Solution Overview

Our solution implements a complete analytical framework:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Pipeline                                │
├─────────────────────────────────────────────────────────────────┤
│  News Data (1.4M headlines) ──► Sentiment Analysis ──► Scores   │
│  Stock Data (6 stocks)      ──► Technical Indicators ──► Signals│
│                             ──► Correlation Analysis ──► Insights│
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

- **Modular Python Package** (`src/`): Reusable functions for data processing, sentiment analysis, and technical indicators
- **Comprehensive Testing**: 35+ unit tests with pytest ensuring code reliability
- **CI/CD Pipeline**: Automated testing and linting with GitHub Actions
- **Interactive Dashboard**: Streamlit app for exploring results

## 📊 Key Results

| Metric | Value | Description |
|--------|-------|-------------|
| Headlines Analyzed | 1,407,328 | Financial news from 2011-2020 |
| Stocks Covered | 6 | AAPL, AMZN, GOOG, META, MSFT, NVDA |
| Sentiment Distribution | 52% neutral, 29% positive, 19% negative | Overall sentiment breakdown |
| Technical Indicators | 6+ | RSI, MACD, SMA, EMA, Bollinger Bands, ATR |
| Test Coverage | 35 tests | All passing with >80% coverage |

### Key Findings

1. **News follows patterns**: Publication timing aligns with market activity (peak at 10 AM and 2 PM)
2. **Sentiment varies by stock**: AMZN and AAPL show most positive sentiment coverage
3. **Technical signals work**: RSI extremes often precede price reversals
4. **Data alignment critical**: Date mismatches limited correlation analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/username/stock-challenge-week1.git
cd stock-challenge-week1

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run app/dashboard.py
```

### Running Tests

```bash
pytest tests/ -v
```

### Running Analysis Notebooks

```bash
jupyter notebook notebooks/
```

## 📁 Project Structure

```
stock-challenge-week1/
├── app/
│   └── dashboard.py          # Streamlit interactive dashboard
├── data/
│   ├── raw/                  # Raw data files
│   └── processed/            # Processed data files
├── notebooks/
│   ├── 00_EDA_Summary.ipynb          # Executive summary
│   ├── 01_Data_Loading_and_Setup.ipynb
│   ├── 02_Descriptive_Statistics.ipynb
│   ├── 03_Text_Analysis.ipynb
│   ├── 04_Time_Series_Analysis.ipynb
│   ├── 05_Publisher_Analysis.ipynb
│   ├── 06_Additional_Analysis.ipynb
│   ├── Quantitative_Analysis.ipynb   # Technical indicators
│   ├── Correlation_Analysis.ipynb    # Sentiment correlation
│   └── figures/                      # Generated visualizations
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration and constants
│   ├── data/
│   │   ├── loader.py         # Data loading functions
│   │   └── preprocessor.py   # Data cleaning functions
│   ├── analysis/
│   │   ├── sentiment.py      # Sentiment analysis (TextBlob, VADER)
│   │   ├── technical.py      # Technical indicators (RSI, MACD, etc.)
│   │   └── statistics.py     # Statistical functions
│   └── visualization/
│       └── plotting.py       # Visualization utilities
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   ├── test_config.py        # Configuration tests
│   └── test_analysis.py      # Analysis function tests
├── scripts/
│   └── md_to_pdf.py          # Markdown to PDF converter
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
├── pytest.ini                # Pytest configuration
├── .flake8                   # Linting configuration
├── INTERIM_REPORT.md         # Progress documentation
├── FINAL_REPORT.md           # Final analysis report
├── GAP_ANALYSIS.md           # Week 12 improvement plan
└── README.md                 # This file
```

## 🔧 Technical Details

### Data Sources

| Dataset | Description | Size |
|---------|-------------|------|
| News Data | Financial News and Stock Price Integration Dataset (FNSPID) | 1.4M headlines |
| Stock Data | Historical OHLCV data for 6 major tech stocks | 2009-2023 |

### Technologies Used

- **Data Processing**: pandas, numpy
- **NLP/Sentiment**: NLTK, TextBlob, VADER
- **Technical Analysis**: Custom implementations (RSI, MACD, SMA, EMA, Bollinger Bands)
- **Visualization**: matplotlib, seaborn, plotly
- **Dashboard**: Streamlit
- **Testing**: pytest, pytest-cov
- **CI/CD**: GitHub Actions

### Technical Indicators Implemented

| Indicator | Description | Use Case |
|-----------|-------------|----------|
| SMA (20, 50, 200) | Simple Moving Average | Trend identification |
| EMA (12, 26) | Exponential Moving Average | Momentum tracking |
| RSI (14) | Relative Strength Index | Overbought/oversold detection |
| MACD | Moving Average Convergence Divergence | Trend changes |
| Bollinger Bands | Price volatility bands | Volatility analysis |
| ATR | Average True Range | Volatility measurement |

## 📈 Demo

### Interactive Dashboard

The Streamlit dashboard allows you to:

- **Select stocks** from AAPL, AMZN, GOOG, META, MSFT, NVDA
- **View technical indicators** with interactive candlestick charts
- **Analyze sentiment** distribution and trends
- **Explore returns** distribution and cumulative performance

```bash
streamlit run app/dashboard.py
```

### Sample Visualizations

<details>
<summary>Click to view sample outputs</summary>

- **Technical Analysis Dashboard**: Price with moving averages, RSI, and MACD
- **Sentiment Distribution**: Positive/Negative/Neutral breakdown by stock
- **Correlation Analysis**: Sentiment vs. Returns scatter plots

</details>

## 🔮 Future Improvements

With more time, we would implement:

1. **Better Date Alignment**: Obtain news data with improved timestamp coverage
2. **Real-time Analysis**: Stream live news and stock data
3. **ML Models**: Train predictive models using sentiment as features
4. **SHAP Explainability**: Add model interpretability visualizations
5. **More Stocks**: Extend coverage to broader market indices
6. **Alternative Aggregation**: Weekly/monthly sentiment windows

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analysis.py -v
```

### Test Coverage

- Configuration module: 10 tests
- Sentiment analysis: 10 tests
- Technical indicators: 5 tests
- Statistical functions: 10 tests

## 📝 Reports

- [Final Report](FINAL_REPORT.md) - Comprehensive analysis findings
- [Interim Report](INTERIM_REPORT.md) - Progress documentation
- [Gap Analysis](GAP_ANALYSIS.md) - Week 12 improvement plan

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Stock Challenge Team**  
10 Academy - Week 1 & Week 12 Challenge  
February 2026

---

*This project demonstrates production-grade data science practices including modular code design, comprehensive testing, CI/CD automation, and interactive visualization - key competencies valued in the finance sector.*
