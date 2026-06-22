import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "db" / "n100.db"
schema_path = BASE_DIR / "db" / "schema.sql"

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys=ON")

with open(schema_path, "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully!")
print("Location:", db_path)