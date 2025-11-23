# EDA Notebook Structure

## Overview

The EDA analysis has been divided into multiple focused notebooks to improve organization, maintainability, and performance. Each notebook focuses on a specific aspect of the analysis.

## Notebook Organization

### 1. `01_Data_Loading_and_Setup.ipynb`
**Purpose:** Initial data loading, data cleaning, preprocessing, and setup

**Sections:**
- **1.1 Data Loading**
  - Load raw CSV file
  - Check initial shape and structure
  - Display first few rows
  
- **1.2 Data Quality Checks**
  - Missing values analysis
  - Duplicate detection (rows, headlines, URLs)
  - Data type verification
  - Date validation
  - Outlier detection (IQR method)
  
- **1.3 Data Cleaning**
  - Handle missing values (report/drop/fill strategy)
  - Remove duplicates
  - Fix invalid dates
  - Handle outliers (if needed)
  
- **1.4 Data Preprocessing**
  - Convert date column to datetime
  - Extract temporal features (year, month, day, day_of_week, hour)
  - Calculate headline metrics (length, word count)
  - Create derived columns
  
- **1.5 Save Processed Data**
  - Save cleaned and preprocessed data to pickle/parquet
  - Document cleaning decisions

**Output:** 
- Cleaned and preprocessed dataframe ready for analysis
- Data quality report
- Saved processed data file

---

### 2. `02_Descriptive_Statistics.ipynb`
**Purpose:** Basic descriptive statistics and distributions
- **1.1 Headline Length Analysis**
  - Character and word count statistics
  - Distribution visualizations
  - Outlier detection
- **1.2 Articles Per Publisher**
  - Publisher activity counts
  - Top publishers identification
  - Long-tail distribution analysis
- **1.3 Publication Date Trends**
  - Yearly, monthly, daily patterns
  - Day of week analysis
  - Publication spike detection

**Dependencies:** `01_Data_Loading_and_Setup.ipynb`

---

### 3. `03_Text_Analysis.ipynb`
**Purpose:** Natural Language Processing and topic modeling
- **2.1 Keyword and Phrase Extraction**
  - Common keywords identification
  - Word frequency analysis
- **2.2 Significant Event Detection**
  - FDA approvals, price targets, earnings, etc.
  - Event pattern matching
- **2.3 Topic Modeling**
  - LDA (Latent Dirichlet Allocation)
  - NMF (Non-negative Matrix Factorization)
  - Topic visualization

**Dependencies:** `01_Data_Loading_and_Setup.ipynb`

---

### 4. `04_Time_Series_Analysis.ipynb`
**Purpose:** Temporal patterns and trends
- **3.1 Publication Frequency Over Time**
  - Hourly, daily, weekly, monthly trends
  - Spike identification
  - Market event correlation
- **3.2 Publishing Time Analysis**
  - Hour of day patterns
  - Day of week patterns
  - Time-of-day heatmaps

**Dependencies:** `01_Data_Loading_and_Setup.ipynb`

---

### 5. `05_Publisher_Analysis.ipynb`
**Purpose:** Deep dive into publisher characteristics
- **4.1 Top Contributing Publishers**
  - Publisher statistics and rankings
  - Articles per day analysis
  - Coverage diversity
- **4.2 News Type Differences by Publisher**
  - Event distribution by publisher
  - Publisher specialization analysis
- **4.3 Email Domain Analysis**
  - Domain extraction and analysis
  - Organizational patterns

**Dependencies:** `01_Data_Loading_and_Setup.ipynb`, `03_Text_Analysis.ipynb` (for event detection)

---

### 6. `06_Additional_Analysis.ipynb` (Optional)
**Purpose:** Supplementary analyses
- Stock-specific analysis
- Publisher-stock relationships
- Data quality checks
- Cross-analysis insights

**Dependencies:** All previous notebooks

---

### 7. `00_EDA_Summary.ipynb` (Optional)
**Purpose:** Executive summary and key findings
- High-level overview
- Key insights from all analyses
- Summary visualizations
- Recommendations

**Dependencies:** All analysis notebooks

---

## Workflow

### Recommended Execution Order:
1. **First:** Run `01_Data_Loading_and_Setup.ipynb` to prepare data
2. **Then:** Run notebooks 2-5 in parallel (they're independent after step 1)
3. **Finally:** Run `06_Additional_Analysis.ipynb` and `00_EDA_Summary.ipynb`

### Data Sharing Between Notebooks:
- **Option 1:** Save processed data to pickle/parquet files
  ```python
  df.to_pickle('data/processed/df_processed.pkl')
  # Load in other notebooks:
  df = pd.read_pickle('data/processed/df_processed.pkl')
  ```

- **Option 2:** Use a shared data loading cell in each notebook
  ```python
  # Standard data loading cell (copy to each notebook)
  import pandas as pd
  df = pd.read_csv('../data/raw_analyst_ratings.csv')
  # ... preprocessing steps ...
  ```

---

## Benefits of This Structure

✅ **Modularity:** Each notebook focuses on one aspect  
✅ **Performance:** Can run notebooks in parallel  
✅ **Maintainability:** Easier to find and fix issues  
✅ **Collaboration:** Multiple people can work on different notebooks  
✅ **Version Control:** Smaller files are easier to track changes  
✅ **Selective Execution:** Run only what you need  

---

## File Naming Convention

- `00_` = Summary/Overview notebooks
- `01_` = Setup/Data loading
- `02-06_` = Analysis notebooks (in logical order)
- Numbers ensure proper ordering in file browsers

---

## Tips

1. **Save intermediate results:** Use pickle/parquet for processed data
2. **Document assumptions:** Add markdown cells explaining your approach
3. **Version control:** Commit after completing each notebook
4. **Test independently:** Each notebook should be runnable standalone (after data loading)

