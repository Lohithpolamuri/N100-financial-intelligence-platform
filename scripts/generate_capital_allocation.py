"""
Sprint 2 - Day 11
Generate Capital Allocation Report

Reads data from SQLite and prepares
capital allocation analysis.
"""

from pathlib import Path
import sqlite3
import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "capital_allocation.csv"

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("DAY 11 - CAPITAL ALLOCATION ENGINE")
print("=" * 60)

# ==========================================================
# LOAD TABLES
# ==========================================================

cashflow = pd.read_sql_query(
    """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """,
    conn
)

profitloss = pd.read_sql_query(
    """
    SELECT
        company_id,
        year,
        net_profit,
        operating_profit,
        sales
    FROM profitandloss
    """,
    conn
)

print(f"Cashflow Records      : {len(cashflow)}")
print(f"Profit & Loss Records : {len(profitloss)}")
# ==========================================================
# IMPORT KPI FUNCTIONS
# ==========================================================

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capital_allocation_pattern,
)

# ==========================================================
# MERGE CASHFLOW & PROFITLOSS
# ==========================================================

merged = pd.merge(
    cashflow,
    profitloss,
    on=["company_id", "year"],
    how="left"
)

print(f"Merged Records        : {len(merged)}")

# ==========================================================
# GENERATE CAPITAL ALLOCATION DATA
# ==========================================================

results = []

for _, row in merged.iterrows():

    fcf = free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    )

    quality_score, quality_label = cfo_quality_score(
        row["operating_activity"],
        row["net_profit"]
    )

    cfo_sign, cfi_sign, cff_sign, pattern = capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        quality_score
    )

    results.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": pattern,
    })

capital_df = pd.DataFrame(results)

print(f"Generated Records     : {len(capital_df)}")
# ==========================================================
# SAVE CSV
# ==========================================================

capital_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"CSV Saved            : {OUTPUT_FILE}")

# ==========================================================
# CLOSE DATABASE
# ==========================================================

conn.close()

print("=" * 60)
print("DAY 11 COMPLETED SUCCESSFULLY")
print("=" * 60)