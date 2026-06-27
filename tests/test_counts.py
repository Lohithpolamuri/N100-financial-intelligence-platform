from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "n100.db"


def get_count(table_name):
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    conn.close()
    return count


def test_companies_count():
    assert get_count("companies") > 0


def test_balancesheet_count():
    assert get_count("balancesheet") > 0


def test_profitandloss_count():
    assert get_count("profitandloss") > 0


def test_cashflow_count():
    assert get_count("cashflow") > 0


def test_stock_prices_count():
    assert get_count("stock_prices") > 0


def test_market_cap_count():
    assert get_count("market_cap") > 0


def test_financial_ratios_count():
    assert get_count("financial_ratios") > 0


def test_peer_groups_count():
    assert get_count("peer_groups") > 0


def test_analysis_count():
    assert get_count("analysis") > 0


def test_sectors_count():
    assert get_count("sectors") > 0