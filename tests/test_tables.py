from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"


def table_exists(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def test_companies_table():
    assert table_exists("companies")


def test_balancesheet_table():
    assert table_exists("balancesheet")


def test_profitandloss_table():
    assert table_exists("profitandloss")


def test_cashflow_table():
    assert table_exists("cashflow")


def test_stock_prices_table():
    assert table_exists("stock_prices")


def test_market_cap_table():
    assert table_exists("market_cap")


def test_financial_ratios_table():
    assert table_exists("financial_ratios")


def test_peer_groups_table():
    assert table_exists("peer_groups")


def test_analysis_table():
    assert table_exists("analysis")


def test_sectors_table():
    assert table_exists("sectors")