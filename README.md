# Data Mining Midterm Project - Apriori Algorithm Implementation

**Student ID:** BV269

##  Project Overview

This project implements and compares three different **frequent itemset mining algorithms** for market basket analysis:

1. **Brute Force Algorithm** - Exhaustive search through all possible item combinations
2. **Apriori Algorithm** - Efficient level-wise candidate generation using downward closure property
3. **FP-Growth Algorithm** - Pattern tree-based mining without candidate generation

The project analyzes transaction data from 5 different retail domains to discover frequent itemsets and generate association rules.

## Datasets

All datasets are in CSV format with columns `Item1` through `Item7`:

| Dataset | File | Transactions | Description |
|---------|------|--------------|-------------|
| Grocery | `grocerytransactions.csv` | 50 | Supermarket purchases (bread, milk, eggs, etc.) |
| Shopping | `shoppingtransactions.csv` | 52 | Clothing store purchases (jeans, shirts, shoes, etc.) |
| Cafe | `cafetransactions.csv` | 50 | Coffee shop orders (coffee, cookies, muffins, etc.) |
| Restaurant | `restauranttransactions.csv` | 50 | Restaurant orders (appetizers, mains, desserts, etc.) |
| Bookstore | `bookstoretransactions.csv` | 50 | Bookstore purchases (same as grocery for demo) |

##  Project Structure

```
datamining-midproj-bv269/
├── MIDPROJ.ipynb           # Main Jupyter notebook with all algorithms
├── REPORT_BV269.pdf        # Detailed project report
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── test_csv.py            # Test script for CSV validation
├── .gitignore             # Git ignore file
└── DATASETS/              # Transaction data folder
    ├── grocerytransactions.csv
    ├── shoppingtransactions.csv
    ├── cafetransactions.csv
    ├── restauranttransactions.csv
    └── bookstoretransactions.csv
```

##  Complete Setup Guide (From Scratch)

### Step 1: Install Python (if not already installed)

1. **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **During installation:**
   -  Check "Add Python to PATH"
   -  Check "Install pip"
3. **Verify installation:**
   ```bash
   python --version
   pip --version
   ```

### Step 2: Install Jupyter Notebook

```bash
pip install jupyter notebook
```

### Step 3: Clone or Download This Project

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/BhavanaVuttunoori/DataMining-Apriori-Algorithm.git
cd DataMining-Apriori-Algorithm
```

**Option B: Download ZIP**
1. Click "Code" → "Download ZIP" on GitHub
2. Extract the ZIP file
3. Open terminal/command prompt in the extracted folder

### Step 4: Install Required Libraries

```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install pandas mlxtend numpy jupyter
```

### Step 5: Launch Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your web browser at `http://localhost:8888`

### Step 6: Open and Run the Project

1. **In Jupyter browser interface:**
   - Click on `MIDPROJ.ipynb` to open the main notebook
   
2. **Run the notebook:**
   - Click "Cell" → "Run All" OR
   - Run cells one by one using `Shift + Enter`

3. **Interactive execution:**
   - The notebook will prompt you to select:
     - Dataset (1-5)
     - Minimum support threshold
     - Minimum confidence threshold  
     - Algorithm choice (Brute Force, Apriori, FP-Growth, or All)

##  How to Use the Notebook

### Cell-by-Cell Execution:

1. **Cell 1 (Imports & Configuration)**
   ```python
   # Run this first to import libraries and set paths
   ```

2. **Cell 2 (Helper Functions)**
   ```python
   # Defines data loading and utility functions
   ```

3. **Cell 3 (Brute Force Algorithm)**
   ```python
   # Implementation of exhaustive search algorithm
   ```

4. **Cell 4 (Apriori & FP-Growth)**
   ```python
   # Wrapper functions for mlxtend library algorithms
   ```

5. **Cell 5 (Main Analyzer)**
   ```python
   # Core function that runs selected algorithms and saves results
   ```

6. **Cell 6 (Interactive Execution)**
   ```python
   # Run this cell to start interactive analysis
   # Follow the prompts to select dataset and parameters
   ```

### Sample Execution Flow:

```
Available datasets:
  1. grocery -> grocerytransactions.csv
  2. shopping -> shoppingtransactions.csv
  3. cafe -> cafetransactions.csv
  4. restaurant -> restauranttransactions.csv
  5. bookstore -> bookstoretransactions.csv

Enter dataset number (1-5): 1
Enter minimum support (percent or fraction): 20
Enter minimum confidence (percent or fraction): 60

Choose algorithm(s) to run:
  1. Brute-force
  2. Apriori (mlxtend)
  3. FP-Growth (mlxtend)
  4. All
Enter choice (1-4): 4
```

##  Understanding the Output

### Console Output:
- **Loading information:** Dataset path, number of transactions loaded
- **Algorithm performance:** Number of frequent itemsets found, execution time
- **File locations:** Where Excel results are saved

### Generated Files:
- `{dataset}_{algorithm}_frequent_itemsets.xlsx` - All frequent itemsets with support values
- `{dataset}_{algorithm}_rules.xlsx` - Association rules with confidence values

### Sample Results:
```
[Brute] Found 15 frequent itemsets in 0.703s
[Apriori] Found 15 frequent itemsets in 0.045s
[FP-Growth] Found 15 frequent itemsets in 0.032s
```

##  Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'mlxtend'**
   ```bash
   pip install mlxtend
   ```

2. **Jupyter not found**
   ```bash
   pip install jupyter
   ```

3. **Permission errors on Windows**
   - Run command prompt as Administrator
   - Or use: `python -m pip install --user [package]`

4. **Path issues**
   - Update `BASE_PATH` in Cell 1 to match your folder location
   - Use forward slashes `/` or raw strings `r"path"`

### Verification Steps:

1. **Test CSV loading:**
   ```bash
   python test_csv.py
   ```

2. **Check installed packages:**
   ```bash
   pip list | grep -E "(pandas|mlxtend|numpy|jupyter)"
   ```

##  Algorithm Details

### 1. Brute Force Algorithm
- **Method:** Exhaustive enumeration of all possible itemsets
- **Time Complexity:** O(2^n) where n is number of unique items
- **Best for:** Small datasets, educational purposes
- **Advantage:** Simple to understand and implement
- **Disadvantage:** Exponential time complexity

### 2. Apriori Algorithm
- **Method:** Level-wise candidate generation using downward closure property
- **Time Complexity:** O(k * C^k) where k is max itemset size, C is candidates
- **Best for:** Medium datasets with moderate item counts
- **Advantage:** Pruning reduces search space significantly
- **Disadvantage:** Multiple database scans, candidate generation overhead

### 3. FP-Growth Algorithm  
- **Method:** Pattern tree construction without candidate generation
- **Time Complexity:** O(n * log(n)) in best case
- **Best for:** Large datasets, dense data
- **Advantage:** Only 2 database scans, no candidate generation
- **Disadvantage:** Memory intensive for sparse data

##  Performance Comparison

| Algorithm | Time (Grocery 50 trans) | Memory Usage | Scalability |
|-----------|------------------------|--------------|-------------|
| Brute Force | 0.703s | Low | Poor |
| Apriori | 0.045s | Medium | Good |
| FP-Growth | 0.032s | High | Excellent |

##  Key Learning Outcomes

1. **Market Basket Analysis:** Understanding customer purchasing patterns
2. **Algorithm Comparison:** Performance trade-offs between different approaches  
3. **Data Mining Concepts:** Support, confidence, frequent itemsets, association rules
4. **Implementation Skills:** Python, pandas, data processing, algorithm optimization
5. **Result Interpretation:** Actionable insights from transaction data

## 👥 Support

- **Issues:** Create an issue on GitHub repository
- **Questions:** Check the project report `REPORT_BV269.pdf` for detailed explanations
- **Code:** All functions are documented with docstrings in the notebook

