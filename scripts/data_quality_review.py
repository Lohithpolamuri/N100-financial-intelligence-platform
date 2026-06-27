from pathlib import Path
import sqlite3
import pandas as pd
import random

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

# =====================================================
# 5 RANDOM COMPANIES
# =====================================================

companies = pd.read_sql("SELECT company_id, company_name FROM companies", conn)

sample = companies.sample(5, random_state=42)

print("=" * 60)
print("5 RANDOM COMPANIES")
print("=" * 60)
print(sample)

# =====================================================
# YEAR COVERAGE
# =====================================================

print("\n")
print("=" * 60)
print("YEAR COVERAGE")
print("=" * 60)

coverage = pd.read_sql("""
SELECT
company_id,
MIN(year) AS first_year,
MAX(year) AS last_year,
COUNT(*) AS total_years
FROM balancesheet
GROUP BY company_id
ORDER BY company_id
""", conn)

print(coverage)

# =====================================================
# LESS THAN 5 YEARS
# =====================================================

print("\n")
print("=" * 60)
print("COMPANIES WITH LESS THAN 5 YEARS")
print("=" * 60)

less5 = coverage[coverage["total_years"] < 5]

print(less5)

conn.close()

print("\nReview Completed Successfully")