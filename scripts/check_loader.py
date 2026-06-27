from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

tables = [
    "companies",
    "balancesheet",
    "profitandloss",
    "cashflow",
    "stock_prices",
    "market_cap",
    "financial_ratios",
    "peer_groups",
    "analysis",
    "sectors"
]

print("=" * 60)
print("LOADER VALIDATION")
print("=" * 60)

errors = 0

for table in tables:
    try:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"✓ {table:<20} {count} rows")
    except Exception as e:
        errors += 1
        print(f"✗ {table}: {e}")

conn.close()

print("\n==========================")

if errors == 0:
    print("No Loader Bugs Found ✅")
else:
    print(f"{errors} Loader Bug(s) Found")

print("==========================")