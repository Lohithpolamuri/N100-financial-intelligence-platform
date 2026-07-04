"""
Sprint 2 - Day 14
Final Validation
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("=" * 60)
print("SPRINT 2 FINAL VALIDATION")
print("=" * 60)

print(f"Total Ratio Rows : {len(ratios)}")

print("\nChecking KPI Columns...\n")

for column in ratios.columns[2:]:
    nulls = ratios[column].isna().sum()
    print(f"{column:<35} NULL Values : {nulls}")

conn.close()