from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("=" * 50)
print("NIFTY100 DATABASE")
print("=" * 50)

for table in tables:
    name = table[0]
    count = conn.execute(
        f"SELECT COUNT(*) FROM {name}"
    ).fetchone()[0]

    print(f"{name:<20} {count}")

conn.close()