from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_key_check")

rows = cursor.fetchall()

if len(rows) == 0:
    print("✓ No Foreign Key Violations Found")
else:
    print("Foreign Key Violations:")
    for row in rows:
        print(row)

conn.close()