from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"


def test_database_exists():
    assert DB_PATH.exists()


def test_database_connection():
    conn = sqlite3.connect(DB_PATH)
    assert conn is not None
    conn.close()


def test_database_readable():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name FROM sqlite_master")
    assert cursor.fetchone() is not None
    conn.close()


def test_foreign_keys_enabled():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    value = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    conn.close()
    assert value == 1


def test_sqlite_version():
    conn = sqlite3.connect(DB_PATH)
    version = conn.execute("SELECT sqlite_version()").fetchone()[0]
    conn.close()
    assert version is not None