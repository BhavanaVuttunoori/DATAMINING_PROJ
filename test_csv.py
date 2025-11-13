#!/usr/bin/env python3
"""
Data Mining Midterm Project - Test CSV Files and Run Algorithms
Student: BV269
"""

import os, sys, time, itertools
from collections import defaultdict
import pandas as pd

# Configuration
BASE_PATH = r"C:\Users\vuttunoori bhavana\Desktop\datamining midproj bv269"

DATASETS = {
    "1": ("grocery", "grocerytransactions.csv"),
    "2": ("shopping", "shoppingtransactions.csv"),
    "3": ("cafe", "cafetransactions.csv"),
    "4": ("restaurant", "restauranttransactions.csv"),
    "5": ("bookstore", "bookstoretransactions.csv")
}

ITEM_COLUMNS = [f"Item{i}" for i in range(1, 8)]

def load_transactions_csv(fullpath):
    """Load transactions from CSV file"""
    print(f"Loading: {fullpath}")
    df = pd.read_csv(fullpath, dtype=str)
    print(f"CSV shape: {df.shape}")
    print(f"CSV columns: {df.columns.tolist()}")
    
    cols = [c for c in ITEM_COLUMNS if c in df.columns]
    if not cols:
        raise ValueError(f"CSV {fullpath} does not contain expected columns {ITEM_COLUMNS}.")
    
    df = df[cols].fillna("").astype(str)
    for c in cols:
        df[c] = df[c].map(lambda x: x.strip())
    
    transactions = []
    for _, row in df.iterrows():
        items = [it for it in row.tolist() if it and it.lower() not in ("nan","none","")]
        if items:  # Only add non-empty transactions
            transactions.append(sorted(set(items)))
    
    return transactions

def brute_force_frequent_itemsets(transactions, min_support):
    """Brute force algorithm for frequent itemsets"""
    n = len(transactions)
    min_count = max(1, int(min_support * n))
    print(f"Min count threshold: {min_count} (support: {min_support})")
    
    items = sorted({it for t in transactions for it in t})
    print(f"Unique items found: {len(items)}")
    
    freq = {}
    k = 1
    while True:
        found = False
        print(f"Checking itemsets of size {k}...")
        for comb in itertools.combinations(items, k):
            count = sum(1 for t in transactions if set(comb).issubset(t))
            if count >= min_count:
                freq[tuple(comb)] = count
                found = True
        
        print(f"Found {sum(1 for f in freq if len(f) == k)} frequent {k}-itemsets")
        if not found or k > len(items):
            break
        k += 1
    
    return freq, n

def test_dataset(dataset_key="1", min_support=0.3):
    """Test loading and processing a dataset"""
    if dataset_key not in DATASETS:
        print(f"Invalid dataset key: {dataset_key}")
        return
    
    short_name, filename = DATASETS[dataset_key]
    fullpath = os.path.join(BASE_PATH, "DATASETS", filename)
    
    print(f"\n{'='*50}")
    print(f"Testing Dataset: {short_name} ({filename})")
    print(f"{'='*50}")
    
    try:
        # Load transactions
        transactions = load_transactions_csv(fullpath)
        print(f"Loaded {len(transactions)} transactions")
        
        if transactions:
            print(f"Sample transactions (first 3):")
            for i, t in enumerate(transactions[:3]):
                print(f"  {i+1}: {t}")
            
            # Run brute force algorithm
            print(f"\nRunning brute force algorithm (min_support={min_support})...")
            start_time = time.time()
            freq_itemsets, n = brute_force_frequent_itemsets(transactions, min_support)
            end_time = time.time()
            
            print(f"Found {len(freq_itemsets)} frequent itemsets in {end_time-start_time:.3f}s")
            
            # Show results by size
            for k in range(1, 6):  # Show up to 5-itemsets
                k_itemsets = [(f, freq_itemsets[f]) for f in freq_itemsets if len(f) == k]
                if k_itemsets:
                    print(f"\n{k}-itemsets ({len(k_itemsets)} found):")
                    for itemset, count in sorted(k_itemsets, key=lambda x: x[1], reverse=True)[:5]:
                        support = count / n
                        print(f"  {itemset}: count={count}, support={support:.3f}")
                    if len(k_itemsets) > 5:
                        print(f"  ... and {len(k_itemsets)-5} more")
        
    except Exception as e:
        print(f"Error processing dataset: {e}")

def main():
    print("Data Mining Midterm Project - CSV Testing")
    print("Student: BV269")
    print(f"Base path: {BASE_PATH}")
    
    # Test all datasets
    for key in ["1", "2", "3", "4", "5"]:
        test_dataset(key, min_support=0.2)  # Lower support for more results

if __name__ == "__main__":
    main()