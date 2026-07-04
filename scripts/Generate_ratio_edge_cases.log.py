"""
Sprint 2 - Day 13
Generate Ratio Edge Case Log
"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

log_path = OUTPUT_DIR / "ratio_edge_cases.log"

with open(log_path, "w") as log:

    log.write("SPRINT 2 - RATIO EDGE CASE REPORT\n")
    log.write("=" * 60 + "\n\n")

    for _, row in ratios.iterrows():

        if row["return_on_equity_pct"] is None:
            log.write(
                f"{row['company_id']} | {row['year']} | "
                "ROE unavailable (invalid equity)\n"
            )

        if row["interest_coverage"] is None:
            log.write(
                f"{row['company_id']} | {row['year']} | "
                "Interest Coverage unavailable (debt free)\n"
            )

        if row["debt_to_equity"] is None:
            log.write(
                f"{row['company_id']} | {row['year']} | "
                "Debt to Equity unavailable\n"
            )

print("=" * 60)
print("EDGE CASE LOG GENERATED")
print("=" * 60)
print(log_path)

conn.close()