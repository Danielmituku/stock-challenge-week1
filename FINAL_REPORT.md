# Financial News Sentiment & Stock Price Analysis
## A Production-Grade Data Science Portfolio Project

**Author:** Daniel Mituku  
**Project:** Week 1 Stock Challenge (Enhanced Week 12)  
**Date:** February 17, 2026  
**Repository:** https://github.com/Danielmituku/stock-challenge-week1

---

## Executive Summary

This project analyzes the relationship between financial news sentiment and stock price movements for six major tech stocks. Originally developed in Week 1, it has been transformed in Week 12 into a **production-grade portfolio piece** demonstrating software engineering best practices valued by finance sector employers.

### Key Achievements

| Metric | Week 1 | Week 12 | Improvement |
|--------|--------|---------|-------------|
| Code Structure | 1 file (398 lines) | 8 modules (1,200+ lines) | 3x more organized |
| Test Coverage | 0 tests | 35 tests | ∞ improvement |
| Type Safety | 0% | 100% functions | Full type hints |
| Documentation | Basic README | Professional docs | Complete overhaul |
| Visualization | Static notebooks | Interactive dashboard | User-accessible |

---

## 1. Business Problem

### The Challenge
**Can we predict stock market movements by analyzing the sentiment of financial news?**

Financial institutions spend billions on market research. Understanding the relationship between news sentiment and price movements could provide:
- **Early warning signals** for price changes
- **Quantified sentiment metrics** for trading decisions
- **Risk assessment tools** for portfolio management

### Stocks Analyzed
| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| AMZN | Amazon.com | E-commerce/Cloud |
| GOOG | Alphabet Inc. | Technology |
| META | Meta Platforms | Social Media |
| MSFT | Microsoft Corp. | Technology |
| NVDA | NVIDIA Corp. | Semiconductors |

---

## 2. Solution Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  News Data (1.4M headlines)          Stock Data (6 tickers)             │
│  └── raw_analyst_ratings.csv         └── AAPL, AMZN, GOOG, META,        │
│      - headline, date, publisher         MSFT, NVDA historical data     │
│      - stock ticker, URL                 - OHLCV daily prices           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER (src/)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  src/data/                    src/analysis/           src/visualization/│
│  ├── loader.py                ├── sentiment.py        └── plotting.py   │
│  │   - load_news_data()       │   - TextBlob                            │
│  │   - load_stock_data()      │   - VADER                               │
│  └── preprocessor.py          ├── technical.py                          │
│      - clean_data()           │   - RSI, MACD, SMA                      │
│      - check_quality()        └── statistics.py                         │
│                                   - correlation                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Streamlit Dashboard (app/dashboard.py)                                 │
│  ├── Price Chart Tab      - Candlestick + indicators                    │
│  ├── Returns Tab          - Distribution + cumulative                   │
│  ├── Sentiment Tab        - Time series + pie chart                     │
│  └── Data Table Tab       - Raw data exploration                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technical Implementation (Week 12 Improvements)

### 3.1 Code Refactoring

**Before (Week 1):** Single utility file with no type hints
```python
# notebooks/utils.py (OLD - no type hints, mixed concerns)
def load_data(file_path='../data/raw.csv', sample_size=None):
    print("Loading dataset...")
    if sample_size:
        df = pd.read_csv(file_path, nrows=sample_size)
    else:
        df = pd.read_csv(file_path)
    return df
```

**After (Week 12):** Modular package with full type hints and dataclasses
```python
# src/data/loader.py (NEW - typed, documented, validated)
from typing import Optional, Union
from pathlib import Path
import pandas as pd
from ..config import DataConfig

def load_news_data(
    file_path: Optional[Union[str, Path]] = None,
    sample_size: Optional[int] = None,
    config: Optional[DataConfig] = None,
) -> pd.DataFrame:
    """
    Load the raw analyst ratings (news) dataset.
    
    Parameters
    ----------
    file_path : str or Path, optional
        Path to the CSV file.
    sample_size : int, optional
        Number of rows to sample.
    config : DataConfig, optional
        Configuration object.
    
    Returns
    -------
    pd.DataFrame
        News data with columns: headline, date, publisher, stock
    
    Raises
    ------
    FileNotFoundError
        If the data file does not exist.
    """
    if config is not None:
        file_path = config.file_path
        sample_size = config.sample_size
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # ... implementation
```

**Configuration Dataclass:**
```python
# src/config.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TechnicalAnalysisConfig:
    """Configuration for technical analysis calculations."""
    
    rsi_period: int = 14
    rsi_overbought: float = 70.0
    rsi_oversold: float = 30.0
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    sma_periods: List[int] = field(default_factory=lambda: [20, 50, 200])
    ema_periods: List[int] = field(default_factory=lambda: [12, 26])
    bollinger_period: int = 20
    bollinger_std: float = 2.0
```

### 3.2 Unit Testing Results

**Test Coverage Summary:**

| Module | Tests | Pass Rate | Coverage |
|--------|-------|-----------|----------|
| `src/config.py` | 12 | 100% | 95% |
| `src/analysis/sentiment.py` | 10 | 100% | 88% |
| `src/analysis/technical.py` | 5 | 100% | 92% |
| `src/analysis/statistics.py` | 8 | 100% | 90% |
| **Total** | **35** | **100%** | **91%** |

**Sample Test Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2
collected 35 items

tests/test_analysis.py::TestSentimentAnalysis::test_textblob_positive PASSED
tests/test_analysis.py::TestSentimentAnalysis::test_vader_negative PASSED
tests/test_analysis.py::TestTechnicalAnalysis::test_calculate_rsi PASSED
tests/test_analysis.py::TestTechnicalAnalysis::test_calculate_macd PASSED
tests/test_analysis.py::TestStatistics::test_gini_coefficient PASSED
tests/test_analysis.py::TestStatistics::test_correlation PASSED
tests/test_config.py::TestDataConfig::test_default_values PASSED
tests/test_config.py::TestDataConfig::test_invalid_config PASSED
... (27 more tests)

============================= 35 passed in 13.91s ==============================
```

### 3.3 Interactive Dashboard

**Dashboard Screenshot Descriptions:**

**Tab 1: Price Chart with Technical Indicators**
```
┌─────────────────────────────────────────────────────────────────┐
│  AAPL Stock Price with Technical Indicators                     │
├─────────────────────────────────────────────────────────────────┤
│  [Candlestick Chart]                                            │
│  - Green/Red candles showing OHLC prices                        │
│  - Orange line: SMA 20-day                                      │
│  - Blue line: SMA 50-day                                        │
│  - Red line: SMA 200-day                                        │
│  - Gray band: Bollinger Bands (±2σ)                             │
├─────────────────────────────────────────────────────────────────┤
│  [RSI Chart - 0 to 100 scale]                                   │
│  - Purple line: RSI value                                       │
│  - Red dashed: Overbought (70)                                  │
│  - Green dashed: Oversold (30)                                  │
├─────────────────────────────────────────────────────────────────┤
│  [MACD Chart]                                                   │
│  - Blue line: MACD                                              │
│  - Orange line: Signal                                          │
│  - Green/Red bars: Histogram                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Tab 2: Returns Distribution**
```
┌────────────────────────────────┬────────────────────────────────┐
│  Daily Returns Distribution    │  Cumulative Returns            │
├────────────────────────────────┼────────────────────────────────┤
│  [Histogram]                   │  [Line Chart]                  │
│  - Bell curve shape            │  - Starting at 1.0             │
│  - Mean: 0.13% daily           │  - Ending at ~3.5x (250%)      │
│  - Std: 1.80%                  │  - Shows growth over time      │
│  - Range: -10% to +12%         │                                │
└────────────────────────────────┴────────────────────────────────┘
```

**Tab 3: Sentiment Analysis**
```
┌────────────────────────────────┬────────────────────────────────┐
│  Sentiment Over Time           │  Category Distribution         │
├────────────────────────────────┼────────────────────────────────┤
│  [Scatter Plot]                │  [Pie Chart]                   │
│  - X: Date                     │  - Green: Positive (29%)       │
│  - Y: Sentiment (-1 to 1)      │  - Red: Negative (19%)         │
│  - Color: Red/Yellow/Green     │  - Gray: Neutral (52%)         │
│  - Horizontal line at 0        │                                │
└────────────────────────────────┴────────────────────────────────┘
```

**Key Metrics Panel:**
```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Latest Price │ Daily Change │ Volatility   │ RSI          │ Period Return│
│    $185.92   │   +1.23%     │   1.80%      │ 58.4 Neutral │   +156.2%   │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 4. Key Results and Findings

### 4.1 Week 1 Analysis Results

**Dataset Statistics:**

| Metric | Value |
|--------|-------|
| Total Headlines | 1,407,328 |
| Date Range | 2011-2020 |
| Unique Publishers | 3,000+ |
| Average Headline Length | 73 characters |
| Valid Date Records | 3.98% |

**Sentiment Distribution (55,230 analyzed headlines):**

```
Sentiment Category Breakdown:
├── Neutral:  52.13% ████████████████████████████████████████████████████
├── Positive: 28.66% ████████████████████████████
└── Negative: 19.20% ███████████████████
```

**Sentiment by Stock:**

| Stock | Mean Sentiment | Category |
|-------|----------------|----------|
| AMZN | +0.190 | Most Positive |
| NVDA | +0.181 | Very Positive |
| AAPL | +0.177 | Very Positive |
| MSFT | +0.125 | Positive |
| META | +0.098 | Slightly Positive |
| GOOG | +0.017 | Nearly Neutral |

**Technical Indicator Results:**

| Stock | Mean Daily Return | Volatility | Sharpe Ratio | Max Drawdown |
|-------|-------------------|------------|--------------|--------------|
| NVDA | 0.19% | 2.89% | 1.82 | -18.76% |
| AAPL | 0.13% | 1.80% | 1.45 | -12.86% |
| AMZN | 0.13% | 2.18% | 1.21 | -14.05% |
| META | 0.11% | 2.53% | 0.89 | -26.39% |
| MSFT | 0.10% | 1.69% | 1.18 | -14.74% |
| GOOG | 0.09% | 1.73% | 1.04 | -11.10% |

**Correlation Analysis Limitation:**
- Only 0.05-0.13% of trading days had matching news data
- Insufficient sample sizes prevented statistically significant conclusions
- This is an important finding: data alignment is critical for correlation studies

### 4.2 Week 12 Improvement Metrics

**Code Quality Improvements:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Number of modules | 1 | 8 | 8x more modular |
| Lines of code | 398 | 1,247 | Better organization |
| Functions with type hints | 0 | 45 | 100% coverage |
| Documented functions | 12 | 45 | 275% increase |
| Cyclomatic complexity (avg) | N/A | 3.2 | Low complexity |

**Testing Improvements:**

| Metric | Before | After |
|--------|--------|-------|
| Unit tests | 0 | 35 |
| Test pass rate | N/A | 100% |
| Code coverage | 0% | 91% |
| Test execution time | N/A | 13.9s |

**Dashboard Capabilities Added:**

| Feature | Description | Business Value |
|---------|-------------|----------------|
| Stock Selection | 6 tickers available | Flexible analysis |
| Date Range Filter | Custom time windows | Historical comparison |
| Technical Indicators | RSI, MACD, SMA, EMA, BB | Trading signals |
| Sentiment View | Time series + distribution | News impact analysis |
| Data Export | Raw data table | Further analysis |

---

## 5. Business Impact Assessment

### Value for Finance Sector

**1. Risk Reduction Through Testing**
- 35 unit tests ensure calculation accuracy
- Critical for financial applications where errors cost money
- Example: RSI calculation verified against known values

**2. Maintainability for Long-term Use**
- Modular code structure enables easy updates
- Type hints reduce bugs during modifications
- Documentation enables team collaboration

**3. Stakeholder Accessibility**
- Interactive dashboard enables non-technical users to explore data
- No coding required to analyze different stocks or time periods
- Immediate insights without data science expertise

### Quantified Portfolio Value

| Skill Demonstrated | Evidence | Finance Relevance |
|-------------------|----------|-------------------|
| Software Engineering | 8 modular packages | Production-ready code |
| Quality Assurance | 35 tests, 91% coverage | Reliable calculations |
| Data Visualization | Interactive dashboard | Stakeholder communication |
| Documentation | Professional README | Team collaboration |
| Python Proficiency | Type hints, dataclasses | Modern best practices |

---

## 6. Limitations and Honest Assessment

### Data Alignment Challenge

The correlation analysis faced a critical limitation:

```
News Data Coverage:  |████░░░░░░░░░░░░░░░░| 3.98% valid dates
Stock Data Coverage: |████████████████████| 100% trading days

Overlap for Analysis: |░░░░░░░░░░░░░░░░░░░░| 0.05-0.13%
```

**Impact:** Insufficient sample sizes (2-5 observations per stock) prevented statistically significant correlation conclusions.

**Lesson Learned:** Data preprocessing and alignment must be verified BEFORE conducting correlation analysis. This is a common real-world data science challenge.

### What This Project Does NOT Prove

1. ❌ Does NOT prove news sentiment predicts stock prices
2. ❌ Does NOT provide trading recommendations
3. ❌ Does NOT account for market-wide factors

### What This Project DOES Demonstrate

1. ✅ End-to-end data science workflow
2. ✅ Professional software engineering practices
3. ✅ Honest reporting of limitations
4. ✅ Production-ready code structure

---

## 7. Future Improvements

### If Given More Time

| Priority | Improvement | Expected Impact |
|----------|-------------|-----------------|
| 1 | Obtain news data with better date coverage | Enable proper correlation analysis |
| 2 | Add SHAP explainability for any ML models | Increase transparency |
| 3 | Deploy dashboard to cloud (Streamlit Cloud) | Public accessibility |
| 4 | Add real-time data feeds | Live analysis capability |
| 5 | Extend to more stocks/indices | Broader market coverage |

### Recommended Next Steps

```
Phase 1: Data Improvement
└── Obtain news data with timestamps matching trading days

Phase 2: Model Development  
└── Train ML models using sentiment as features
└── Add SHAP visualizations for model explainability

Phase 3: Production Deployment
└── Deploy to cloud platform
└── Add authentication and user management
└── Implement real-time data streaming
```

---

## 8. How to Run This Project

### Quick Start

```bash
# Clone repository
git clone https://github.com/Danielmituku/stock-challenge-week1.git
cd stock-challenge-week1

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Launch dashboard
streamlit run app/dashboard.py
```

### Project Structure

```
stock-challenge-week1/
├── app/
│   └── dashboard.py          # Streamlit dashboard
├── src/
│   ├── config.py             # Configuration dataclasses
│   ├── data/                 # Data loading/preprocessing
│   ├── analysis/             # Sentiment, technical, statistics
│   └── visualization/        # Plotting utilities
├── tests/
│   ├── test_config.py        # 12 tests
│   └── test_analysis.py      # 23 tests
├── notebooks/                # Analysis notebooks
├── INTERIM_REPORT.md         # Progress report
├── FINAL_REPORT.md           # This document
└── README.md                 # Project documentation
```

---

## 9. Conclusion

This project demonstrates the journey from initial data analysis to a production-ready portfolio piece. Key accomplishments:

### Technical Excellence
- **8 modular packages** with full type hints
- **35 unit tests** with 91% coverage
- **Interactive dashboard** for stakeholder engagement

### Professional Standards
- Clean, documented, maintainable code
- Comprehensive testing and validation
- Honest reporting of limitations

### Finance Sector Readiness
- Reliable calculations verified by tests
- Accessible visualizations for non-technical users
- Production-ready architecture

### Honest Assessment
- Data limitations prevented correlation conclusions
- This finding itself demonstrates rigorous data science practice
- Better data would enable the intended analysis

---

**Repository:** https://github.com/Danielmituku/stock-challenge-week1  
**Dashboard:** Run `streamlit run app/dashboard.py`  
**Tests:** Run `pytest tests/ -v` (35 tests, all passing)

---

*This report demonstrates production-grade data science practices including modular code design, comprehensive testing, interactive visualization, and honest communication of limitations—key competencies valued by finance sector employers.*
