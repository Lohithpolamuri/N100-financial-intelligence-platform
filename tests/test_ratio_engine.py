"""
Sprint 2 - Day 13
Ratio Engine Validation Tests
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("DAY 13 - RATIO ENGINE VALIDATION")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
ratio_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT company_id || year) FROM financial_ratios")
unique_count = cursor.fetchone()[0]

print(f"Financial Ratio Rows : {ratio_count}")
print(f"Unique Company-Year  : {unique_count}")

if ratio_count == unique_count:
    print("PASS - No duplicate ratio records")
else:
    print("FAIL - Duplicate ratio records found")

conn.close()