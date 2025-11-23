# EDA Notebooks - Stock Challenge Week 1

This directory contains the Exploratory Data Analysis notebooks for the financial news dataset.

## Quick Start

1. **Start here:** `01_Data_Loading_and_Setup.ipynb`
   - Loads and preprocesses the raw data
   - Run this first before any other notebook

2. **Then run any of these (in any order):**
   - `02_Descriptive_Statistics.ipynb` - Basic stats and distributions
   - `03_Text_Analysis.ipynb` - NLP and topic modeling
   - `04_Time_Series_Analysis.ipynb` - Temporal patterns
   - `05_Publisher_Analysis.ipynb` - Publisher deep dive

3. **Optional:**
   - `06_Additional_Analysis.ipynb` - Supplementary analyses
   - `00_EDA_Summary.ipynb` - Executive summary

## Notebook Structure

See `NOTEBOOK_STRUCTURE.md` for detailed information about each notebook.

## Shared Utilities

The `utils.py` module contains helper functions used across notebooks:
- `load_and_preprocess_data()` - Load and preprocess data
- `save_processed_data()` - Save processed data
- `load_processed_data()` - Load saved processed data
- `setup_plotting_style()` - Configure plotting style
- `gini_coefficient()` - Calculate inequality measure
- `identify_spikes()` - Find spikes in time series
- `extract_email_domain()` - Extract email domains

## Usage Example

```python
# In any notebook, import utilities:
import sys
sys.path.append('.')
from utils import load_and_preprocess_data, setup_plotting_style

# Load data
df = load_and_preprocess_data()

# Setup plotting
setup_plotting_style()

# Your analysis here...
```

## Data Files

- **Input:** `../data/raw_analyst_ratings.csv` (original dataset)
- **Output:** `../data/processed/df_processed.pkl` (saved after preprocessing)
- **Visualizations:** Saved to `notebooks/` directory as PNG files

## Notes

- Each notebook is designed to be run independently (after data loading)
- Notebooks can be run in parallel for faster execution
- Intermediate results can be saved to avoid recomputation

