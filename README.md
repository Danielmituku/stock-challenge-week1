# Stock Challenge - Week 1

Analysis of financial news sentiment and its correlation with stock price movements. This project includes NLP sentiment scoring, data engineering workflows, and statistical analysis to uncover how headline sentiment impacts market behavior.

## Project Overview

This project is divided into three main tasks:

1. **Task 1: Git and GitHub** - Setting up development environment, performing EDA on news data, and implementing CI/CD
2. **Task 2: Quantitative Analysis** - Using PyNance and TA-Lib for technical analysis and financial metrics
3. **Task 3: Correlation Analysis** - Analyzing the relationship between news sentiment and stock price movements

## Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       ├── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stock-challenge-week1
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** TA-Lib requires the C library to be installed first. On macOS:
```bash
brew install ta-lib
```

Then install the Python package:
```bash
pip install TA-Lib
```

## Dependencies

### Core Libraries
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** & **seaborn** - Data visualization

### Natural Language Processing
- **nltk** - Natural language processing toolkit
- **textblob** - Simple NLP library for sentiment analysis
- **vaderSentiment** - Valence Aware Dictionary and sEntiment Reasoner
- **scikit-learn** - Machine learning (for topic modeling)

### Financial Analysis
- **yfinance** - Yahoo Finance API for stock data
- **TA-Lib** - Technical analysis library (RSI, MACD, moving averages)
- **scipy** - Statistical analysis and correlation

### Development Tools
- **jupyter** - Interactive notebooks
- **pytest** - Testing framework
- **black** - Code formatter
- **flake8** - Linting tool

## Tasks

### Task 1: Git and GitHub & EDA

**Objectives:**
- Set up Python development environment
- Perform Exploratory Data Analysis (EDA) on news data
- Implement Git version control and CI/CD

**Key Analyses:**
- Descriptive statistics (headline lengths, article counts per publisher)
- Publication date trends and time series analysis
- Text analysis and topic modeling using NLP
- Publisher analysis

### Task 2: Quantitative Analysis

**Objectives:**
- Load and prepare stock price data
- Calculate technical indicators using TA-Lib (RSI, MACD, moving averages)
- Use PyNance for financial metrics
- Create visualizations of data and indicators

### Task 3: Correlation Analysis

**Objectives:**
- Align news and stock price datasets by date
- Perform sentiment analysis on news headlines
- Calculate daily stock returns
- Analyze correlation between sentiment scores and stock movements

## Usage

### Running Notebooks

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory to access analysis notebooks.

### Running Tests

```bash
pytest tests/
```

### Running Scripts

```bash
python scripts/<script_name>.py
```

## Contributing

1. Create a new branch for your feature: `git checkout -b task-X`
2. Make your changes and commit with descriptive messages
3. Push to your branch: `git push origin task-X`
4. Create a Pull Request to merge into main

## Commit Guidelines

- Commit at least three times a day with descriptive messages
- Use clear, descriptive commit messages
- Follow the branch naming convention: `task-1`, `task-2`, `task-3`

## License

[Add your license here]

## Author

[Add your name/contact information here]
