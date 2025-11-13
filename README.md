# Data Mining Midterm Project - Apriori Algorithm Implementation

**Student ID:** BV269

## Project Overview
Implementation and comparison of frequent itemset mining algorithms (Brute Force, Apriori, FP-Growth) on transaction datasets.

## Datasets
- `grocerytransactions.xlsx` - Grocery store transactions
- `shoppingtransactions.xlsx` - Shopping mall transactions  
- `cafetransactions.xlsx` - Cafe transactions
- `restauranttransactions.xlsx` - Restaurant transactions
- `bookstoretransactions.xlsx` - Bookstore transactions

## Files
- `MIDPROJ.ipynb` - Main implementation notebook
- `REPORT_BV269.pdf` - Project report
- `DATASETS/` - Transaction data files

## Requirements
```bash
pip install pandas openpyxl mlxtend
```

## Usage
1. Open `MIDPROJ.ipynb` in Jupyter
2. Run cells sequentially
3. Select dataset and algorithm parameters when prompted

## Algorithms Implemented
1. **Brute Force** - Complete enumeration approach
2. **Apriori** - Level-wise candidate generation
3. **FP-Growth** - Pattern tree based mining

Results are saved as Excel files with frequent itemsets and association rules.