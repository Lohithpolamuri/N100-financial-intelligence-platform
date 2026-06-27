from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"


def fetch_one(query):
    conn = sqlite3.connect(DB_PATH)
    value = conn.execute(query).fetchone()[0]
    conn.close()
    return value


def test_no_duplicate_company_ids():
    total = fetch_one("SELECT COUNT(company_id) FROM companies")
    unique = fetch_one("SELECT COUNT(DISTINCT company_id) FROM companies")
    assert total == unique


def test_no_null_company_ids():
    assert fetch_one(
        "SELECT COUNT(*) FROM companies WHERE company_id IS NULL"
    ) == 0


def test_foreign_key_check():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    rows = conn.execute("PRAGMA foreign_key_check").fetchall()
    conn.close()
    assert len(rows) == 0


def test_database_has_10_tables():
    assert fetch_one(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
    ) >= 10


def test_companies_not_empty():
    assert fetch_one("SELECT COUNT(*) FROM companies") > 0