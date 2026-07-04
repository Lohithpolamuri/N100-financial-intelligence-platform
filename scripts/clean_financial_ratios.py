import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("CLEANING FINANCIAL RATIOS TABLE")
print("=" * 60)

# Total rows before cleanup
cursor.execute("SELECT COUNT(*) FROM financial_ratios")
before = cursor.fetchone()[0]

print(f"Rows before cleanup : {before}")

# Keep only the best row for each company-year
cursor.execute("""
DELETE FROM financial_ratios
WHERE rowid NOT IN (
    SELECT rowid
    FROM (
        SELECT rowid,
               ROW_NUMBER() OVER (
                   PARTITION BY company_id, year
                   ORDER BY
                       (COALESCE(free_cash_flow_cr,0) != 0) DESC,
                       (COALESCE(capex_cr,0) != 0) DESC,
                       (COALESCE(cash_from_operations_cr,0) != 0) DESC,
                       rowid
               ) AS rn
        FROM financial_ratios
    )
    WHERE rn = 1
);
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
after = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM (
    SELECT company_id, year
    FROM financial_ratios
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
);
""")

duplicates = cursor.fetchone()[0]

print(f"Rows after cleanup  : {after}")
print(f"Duplicates left     : {duplicates}")

print("=" * 60)
print("FINANCIAL RATIOS CLEANUP COMPLETED")
print("=" * 60)

conn.close()