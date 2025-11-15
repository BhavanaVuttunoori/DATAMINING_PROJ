#!/usr/bin/env python3
"""
Data Mining Midterm Project - Apriori Algorithm Implementation
Student ID: BV269

This script implements and compares three frequent itemset mining algorithms:
1. Brute Force - Exhaustive enumeration
2. Apriori - Level-wise candidate generation
3. FP-Growth - Pattern tree based mining
"""

# ==============================================================================
# IMPORTS AND CONFIGURATION
# ==============================================================================

import os, sys, time, itertools
from collections import defaultdict
import pandas as pd

# BASE_PATH: update if different in your environment (use WSL path if using WSL)
BASE_PATH = r"C:\Users\vuttunoori bhavana\Desktop\datamining midproj bv269"

DATASETS = {
    "1": ("grocery", "grocerytransactions.csv"),
    "2": ("shopping", "shoppingtransactions.csv"),
    "3": ("cafe", "cafetransactions.csv"),
    "4": ("restaurant", "restauranttransactions.csv"),
    "5": ("bookstore", "bookstoretransactions.csv")
}

ITEM_COLUMNS = [f"Item{i}" for i in range(1, 8)]


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def validate_base_path(path):
    """Validate that the base path exists"""
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Base path not found: {path}")


def list_datasets():
    """Display available datasets"""
    print("Available datasets:")
    for key, (short, fname) in DATASETS.items():
        print(f"  {key}. {short} -> {fname}")


def load_transactions_csv(fullpath):
    """Load transactions from CSV file"""
    df = pd.read_csv(fullpath, dtype=str)
    cols = [c for c in ITEM_COLUMNS if c in df.columns]
    if not cols:
        raise ValueError(f"CSV {fullpath} does not contain expected columns {ITEM_COLUMNS}.")
    df = df[cols].fillna("").astype(str)
    for c in cols:
        df[c] = df[c].map(lambda x: x.strip())
    transactions = []
    for _, row in df.iterrows():
        items = [it for it in row.tolist() if it and it.lower() not in ("nan","none")]
        transactions.append(sorted(set(items)))
    return transactions


def prepare_onehot_df(transactions):
    """Convert transactions to one-hot encoded DataFrame"""
    all_items = sorted({it for t in transactions for it in t})
    rows = []
    for t in transactions:
        rows.append({item: (item in t) for item in all_items})
    return pd.DataFrame(rows)


def save_itemsets_rules_excel(basepath, dataset_shortname, approach, freq_dict, n, rules):
    """Save frequent itemsets and association rules to Excel files"""
    os.makedirs(basepath, exist_ok=True)
    
    # Save frequent itemsets
    fi_rows = []
    for it, cnt in sorted(freq_dict.items(), key=lambda x: (-x[1], x[0])):
        fi_rows.append({"itemset": "|".join(it), "count": cnt, "support": cnt / n})
    fi_df = pd.DataFrame(fi_rows)
    fi_path = os.path.join(basepath, f"{dataset_shortname}_{approach}_frequent_itemsets.xlsx")
    fi_df.to_excel(fi_path, index=False)

    # Save association rules
    rules_rows = []
    for ant, cons, sup, conf in rules:
        rules_rows.append({"antecedent": "|".join(ant), "consequent": "|".join(cons),
                           "support": sup, "confidence": conf})
    rules_df = pd.DataFrame(rules_rows)
    rules_path = os.path.join(basepath, f"{dataset_shortname}_{approach}_rules.xlsx")
    rules_df.to_excel(rules_path, index=False)
    
    return fi_path, rules_path


# ==============================================================================
# BRUTE-FORCE ALGORITHM
# ==============================================================================

def brute_force_frequent_itemsets(transactions, min_support):
    """
    Brute force algorithm for finding frequent itemsets.
    Exhaustively checks all possible combinations.
    """
    n = len(transactions)
    min_count = max(1, int(min_support * n))
    items = sorted({it for t in transactions for it in t})
    freq = {}
    k = 1
    
    while True:
        found = False
        for comb in itertools.combinations(items, k):
            count = sum(1 for t in transactions if set(comb).issubset(t))
            if count >= min_count:
                freq[tuple(comb)] = count
                found = True
        if not found:
            break
        k += 1
        if k > len(items):
            break
    
    return freq, n


# ==============================================================================
# APRIORI AND FP-GROWTH ALGORITHMS (using mlxtend)
# ==============================================================================

def run_mlxtend_apriori(transactions, min_support, min_confidence):
    """
    Wrapper for mlxtend's Apriori algorithm.
    Uses level-wise candidate generation with pruning.
    """
    try:
        from mlxtend.frequent_patterns import apriori, association_rules
    except Exception as e:
        raise ImportError("mlxtend not available. Install in your environment (see message below).") from e
    
    df = prepare_onehot_df(transactions)
    freq = apriori(df, min_support=min_support, use_colnames=True)
    n = len(transactions)
    
    if freq.empty:
        return {}, n, []
    
    freq_dict = {tuple(sorted(list(s))): int(round(support * n)) 
                 for s, support in zip(freq['itemsets'], freq['support'])}
    
    rules_df = association_rules(freq, metric="confidence", min_threshold=min_confidence)
    rules = []
    for _, row in rules_df.iterrows():
        antecedent = tuple(sorted(list(row['antecedents'])))
        consequent = tuple(sorted(list(row['consequents'])))
        rules.append((antecedent, consequent, float(row['support']), float(row['confidence'])))
    
    return freq_dict, n, rules


def run_mlxtend_fpgrowth(transactions, min_support, min_confidence):
    """
    Wrapper for mlxtend's FP-Growth algorithm.
    Uses FP-tree for efficient pattern mining without candidate generation.
    """
    try:
        from mlxtend.frequent_patterns import fpgrowth, association_rules
    except Exception as e:
        raise ImportError("mlxtend not available. Install in your environment (see message below).") from e
    
    df = prepare_onehot_df(transactions)
    freq = fpgrowth(df, min_support=min_support, use_colnames=True)
    n = len(transactions)
    
    if freq.empty:
        return {}, n, []
    
    freq_dict = {tuple(sorted(list(s))): int(round(support * n)) 
                 for s, support in zip(freq['itemsets'], freq['support'])}
    
    rules_df = association_rules(freq, metric="confidence", min_threshold=min_confidence)
    rules = []
    for _, row in rules_df.iterrows():
        antecedent = tuple(sorted(list(row['antecedents'])))
        consequent = tuple(sorted(list(row['consequents'])))
        rules.append((antecedent, consequent, float(row['support']), float(row['confidence'])))
    
    return freq_dict, n, rules


# ==============================================================================
# MAIN ANALYZER FUNCTION
# ==============================================================================

def analyze_dataset_notebook(basepath, filename, shortname,
                             min_support=0.2, min_confidence=0.6,
                             run_brute=True, run_apriori=True, run_fpgrowth=True):
    """
    Analyze a dataset using selected algorithms.
    Auto-skips library-based algorithms when dependencies are missing.
    """
    fullpath = os.path.join(basepath, filename)
    if not os.path.isfile(fullpath):
        raise FileNotFoundError(f"Dataset not found: {fullpath}")
    
    print(f"\nLoading dataset: {fullpath}")
    transactions = load_transactions_csv(fullpath)
    print(f"Loaded {len(transactions)} transactions. (first 3): {transactions[:3]}")
    results = {}

    # Brute Force Algorithm
    if run_brute:
        t0 = time.time()
        brute_fi, n = brute_force_frequent_itemsets(transactions, min_support)
        t_brute = time.time() - t0
        print(f"[Brute] Found {len(brute_fi)} frequent itemsets in {t_brute:.3f}s")
        
        # Generate association rules
        brute_rules = []
        supports = {it: cnt / n for it, cnt in brute_fi.items()}
        for it, cnt in brute_fi.items():
            if len(it) < 2:
                continue
            for r in range(1, len(it)):
                for ant in itertools.combinations(it, r):
                    ant = tuple(sorted(ant))
                    cons = tuple(sorted(set(it) - set(ant)))
                    ant_sup = supports.get(ant, 0)
                    if ant_sup > 0:
                        conf = supports[it] / ant_sup
                        if conf >= min_confidence:
                            brute_rules.append((ant, cons, supports[it], conf))
        
        fi_path, rules_path = save_itemsets_rules_excel(basepath, shortname, "brute", brute_fi, n, brute_rules)
        print(f"[Brute] Saved files:\n  {fi_path}\n  {rules_path}")
        results['brute'] = {"itemsets": brute_fi, "rules": brute_rules, "time": t_brute}

    # Apriori Algorithm
    if run_apriori:
        try:
            t0 = time.time()
            apriori_fi, n_ap, apriori_rules = run_mlxtend_apriori(transactions, min_support, min_confidence)
            t_ap = time.time() - t0
            print(f"[Apriori] Found {len(apriori_fi)} frequent itemsets in {t_ap:.3f}s")
            ap_paths = save_itemsets_rules_excel(basepath, shortname, "apriori", apriori_fi, n_ap, apriori_rules)
            print(f"[Apriori] Saved files:\n  {ap_paths[0]}\n  {ap_paths[1]}")
            results['apriori'] = {"itemsets": apriori_fi, "rules": apriori_rules, "time": t_ap}
        except ImportError as ie:
            print("Apriori (mlxtend) skipped: mlxtend not installed.")
            print("Install mlxtend in your environment, e.g.:")
            print("  pip install mlxtend")
            results['apriori'] = {"error": "mlxtend_missing"}
        except Exception as e:
            print("Apriori (mlxtend) failed:", e)
            results['apriori'] = {"error": str(e)}

    # FP-Growth Algorithm
    if run_fpgrowth:
        try:
            t0 = time.time()
            fpg_fi, n_fp, fpg_rules = run_mlxtend_fpgrowth(transactions, min_support, min_confidence)
            t_fp = time.time() - t0
            print(f"[FP-Growth] Found {len(fpg_fi)} frequent itemsets in {t_fp:.3f}s")
            fpg_paths = save_itemsets_rules_excel(basepath, shortname, "fpgrowth", fpg_fi, n_fp, fpg_rules)
            print(f"[FP-Growth] Saved files:\n  {fpg_paths[0]}\n  {fpg_paths[1]}")
            results['fpgrowth'] = {"itemsets": fpg_fi, "rules": fpg_rules, "time": t_fp}
        except ImportError as ie:
            print("FP-Growth (mlxtend) skipped: mlxtend not installed.")
            print("Install mlxtend in your environment, e.g.:")
            print("  pip install mlxtend")
            results['fpgrowth'] = {"error": "mlxtend_missing"}
        except Exception as e:
            print("FP-Growth (mlxtend) failed:", e)
            results['fpgrowth'] = {"error": str(e)}

    return results


# ==============================================================================
# MAIN EXECUTION (Interactive)
# ==============================================================================

def main():
    """Main function for interactive execution"""
    print("="*60)
    print("Data Mining Midterm Project - Market Basket Analysis")
    print("Student ID: BV269")
    print("="*60)
    
    # List available datasets
    list_datasets()
    choice = input("\nEnter dataset number (1-5): ").strip()
    if choice not in DATASETS:
        raise ValueError("Invalid choice")
    filename, shortname = DATASETS[choice][1], DATASETS[choice][0]

    # Get support and confidence thresholds
    s = input("Enter minimum support (percent or fraction): ").strip()
    c = input("Enter minimum confidence (percent or fraction): ").strip()
    s = float(s)/100.0 if float(s) > 1 else float(s)
    c = float(c)/100.0 if float(c) > 1 else float(c)

    # Choose algorithm(s)
    print("\nChoose algorithm(s) to run:")
    print("  1. Brute-force")
    print("  2. Apriori (mlxtend)")
    print("  3. FP-Growth (mlxtend)")
    print("  4. All")
    algo_choice = input("Enter choice (1-4): ").strip()
    if algo_choice not in ("1","2","3","4"):
        algo_choice = "4"
    
    run_brute = algo_choice in ("1","4")
    run_apriori = algo_choice in ("2","4")
    run_fpgrowth = algo_choice in ("3","4")

    # Run analysis
    results = analyze_dataset_notebook(BASE_PATH, filename, shortname,
                                      min_support=s, min_confidence=c,
                                      run_brute=run_brute, run_apriori=run_apriori, 
                                      run_fpgrowth=run_fpgrowth)

    print("\n" + "="*60)
    print("Analysis Complete!")
    print(f"Results keys: {results.keys()}")
    print("="*60)


if __name__ == "__main__":
    main()
