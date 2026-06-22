import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM companies")
print("Companies:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM balancesheet")
print("BalanceSheet:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM profitandloss")
print("ProfitLoss:", cursor.fetchone()[0])

conn.close()