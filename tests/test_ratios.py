from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)


# 1. Net Profit Margin - Normal Case
def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


# 2. Net Profit Margin - Zero Sales
def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# 3. Operating Profit Margin - Normal Case
def test_operating_profit_margin_normal():
    assert operating_profit_margin(200, 1000) == 20.0


# 4. Operating Profit Margin - Mismatch Logging
def test_operating_profit_margin_mismatch():
    result = operating_profit_margin(200, 1000, expected_opm=25)
    assert result == 20.0


# 5. ROE - Normal Case
def test_return_on_equity_normal():
    assert return_on_equity(150, 500, 500) == 15.0


# 6. ROE - Negative Equity
def test_return_on_equity_negative():
    assert return_on_equity(100, -200, 100) is None


# 7. ROCE - Normal Case
def test_return_on_capital_employed():
    assert return_on_capital_employed(
        200,
        500,
        300,
        200
    ) == 20.0


# 8. ROA - Zero Assets
def test_return_on_assets_zero():
    assert return_on_assets(100, 0) is None