from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"


def get_columns(table):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols


def test_companies_company_id():
    assert "company_id" in get_columns("companies")


def test_balancesheet_company_id():
    assert "company_id" in get_columns("balancesheet")


def test_profitandloss_company_id():
    assert "company_id" in get_columns("profitandloss")


def test_cashflow_company_id():
    assert "company_id" in get_columns("cashflow")


def test_stock_prices_company_id():
    assert "company_id" in get_columns("stock_prices")