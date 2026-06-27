from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"
OUTPUT_PATH = BASE_DIR / "output"

OUTPUT_PATH.mkdir(exist_ok=True)

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

audit = []

print("\n========== LOAD AUDIT ==========\n")

for table in tables:
    count = pd.read_sql_query(
        f"SELECT COUNT(*) AS count FROM {table}",
        conn
    ).iloc[0]["count"]

    audit.append({
        "table_name": table,
        "row_count": count
    })

    print(f"{table:<20} {count}")

audit_df = pd.DataFrame(audit)

audit_df.to_csv(
    OUTPUT_PATH / "load_audit.csv",
    index=False
)

print("\nload_audit.csv created successfully!")

conn.close()