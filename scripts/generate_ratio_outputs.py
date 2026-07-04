"""
Sprint 2 - Day 13
Generate Capital Allocation CSV
and Ratio Edge Case Log
"""
from src.analytics.cashflow_kpis import capital_allocation_pattern
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("DAY 13 - OUTPUT GENERATION")
print("=" * 60)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

print(f"Financial Ratios : {len(ratios)}")
print(f"Cashflow Records : {len(cashflow)}")
# ==========================================================
# MERGE CASHFLOW
# ==========================================================
cashflow_unique = cashflow.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

capital = ratios.merge(
    cashflow_unique,
    on=["company_id", "year"],
    how="left"
)

print(f"Merged Rows : {len(capital)}")
# ==========================================================
# CAPITAL ALLOCATION PATTERN
# ==========================================================

patterns = []

for _, row in capital.iterrows():

    cfo, cfi, cff, label = capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    )

    patterns.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": cfo,
        "cfi_sign": cfi,
        "cff_sign": cff,
        "capital_allocation_pattern": label
    })

pattern_df = pd.DataFrame(patterns)

print(f"Capital Allocation Rows : {len(pattern_df)}")
# ==========================================================
# SAVE CSV
# ==========================================================

csv_path = OUTPUT_DIR / "capital_allocation.csv"

pattern_df.to_csv(
    csv_path,
    index=False
)

print(f"Saved : {csv_path}")