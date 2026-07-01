from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


# ==========================================================
# FREE CASH FLOW
# ==========================================================

def test_free_cash_flow():
    assert free_cash_flow(1000, -300) == 700


# ==========================================================
# CFO QUALITY SCORE
# ==========================================================

def test_cfo_quality_high():
    score, label = cfo_quality_score(120, 100)
    assert score == 1.20
    assert label == "High Quality"


def test_cfo_quality_moderate():
    score, label = cfo_quality_score(75, 100)
    assert score == 0.75
    assert label == "Moderate"


def test_cfo_quality_accrual():
    score, label = cfo_quality_score(30, 100)
    assert score == 0.30
    assert label == "Accrual Risk"


def test_cfo_quality_zero_pat():
    score, label = cfo_quality_score(100, 0)
    assert score is None
    assert label is None


# ==========================================================
# CAPEX INTENSITY
# ==========================================================

def test_capex_asset_light():
    value, label = capex_intensity(-20, 1000)
    assert value == 2.00
    assert label == "Asset Light"


def test_capex_moderate():
    value, label = capex_intensity(-50, 1000)
    assert value == 5.00
    assert label == "Moderate"


def test_capex_capital_intensive():
    value, label = capex_intensity(-120, 1000)
    assert value == 12.00
    assert label == "Capital Intensive"


# ==========================================================
# FCF CONVERSION
# ==========================================================

def test_fcf_conversion():
    assert fcf_conversion_rate(500, 1000) == 50.00


# ==========================================================
# CAPITAL ALLOCATION PATTERN
# ==========================================================

def test_capital_allocation_pattern():
    cfo, cfi, cff, label = capital_allocation_pattern(
        1000,
        -500,
        -200,
        1.2
    )

    assert cfo == "+"
    assert cfi == "-"
    assert cff == "-"
    assert label == "Shareholder Returns"