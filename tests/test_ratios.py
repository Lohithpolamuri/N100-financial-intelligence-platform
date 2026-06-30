from src.analytics.ratios import *

# ----------------------------
# DAY 8 TESTS
# ----------------------------

def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0


def test_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_opm():
    assert operating_profit_margin(200, 1000) == 20.0


def test_roe_negative():
    assert return_on_equity(100, -200, 100) is None


def test_roce():
    assert return_on_capital_employed(
        200,
        500,
        300,
        200
    ) == 20.0


def test_roa_zero():
    assert return_on_assets(100, 0) is None


def test_opm_crosscheck():
    assert operating_profit_margin(
        200,
        1000,
        expected_opm=20
    ) == 20.0


def test_roe():
    assert return_on_equity(
        150,
        500,
        500
    ) == 15.0


# ----------------------------
# DAY 9 TESTS
# ----------------------------

def test_debt_free_returns_zero():
    assert debt_to_equity(0, 100, 100) == 0


def test_high_de_flag():
    assert high_leverage_flag(
        6,
        "Technology"
    ) is True


def test_financial_no_flag():
    assert high_leverage_flag(
        10,
        "Financials"
    ) is False


def test_interest_zero():
    assert interest_coverage_ratio(
        100,
        50,
        0
    ) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning_flag(1.2) is True


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(
        1000,
        500
    ) == 2.0