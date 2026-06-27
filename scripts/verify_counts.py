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

print("=" * 50)
print("DATABASE VERIFICATION")
print("=" * 50)

for table in tables:
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20} {count}")

conn.close()

print("\n✓ Verification Completed Successfully")