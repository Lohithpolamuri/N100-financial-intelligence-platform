"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

from typing import Optional


# ==========================================================
# FREE CASH FLOW
# ==========================================================

def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow = CFO + Investing Activity
    Negative values are allowed.
    """
    return operating_activity + investing_activity


# ==========================================================
# CFO QUALITY SCORE
# ==========================================================

def cfo_quality_score(
    cfo_average: float,
    pat_average: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CFO / PAT Quality Score
    """

    if pat_average == 0:
        return None, None

    score = round(cfo_average / pat_average, 2)

    if score > 1.0:
        label = "High Quality"
    elif score >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return score, label


# ==========================================================
# CAPEX INTENSITY
# ==========================================================

def capex_intensity(
    investing_activity: float,
    sales: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CapEx Intensity
    """

    if sales == 0:
        return None, None

    intensity = round(abs(investing_activity) / sales * 100, 2)

    if intensity < 3:
        label = "Asset Light"
    elif intensity <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return intensity, label


# ==========================================================
# FCF CONVERSION RATE
# ==========================================================

def fcf_conversion_rate(
    free_cash_flow_value: float,
    operating_profit: float
) -> Optional[float]:
    """
    FCF Conversion Rate
    """

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow_value / operating_profit * 100,
        2
    )
# ==========================================================
# CAPITAL ALLOCATION PATTERN CLASSIFIER
# ==========================================================

def _cashflow_sign(value: float) -> str:
    """
    Returns '+' for positive or zero values and '-' for negative values.
    """
    return "+" if value >= 0 else "-"


def capital_allocation_pattern(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    cfo_quality: float | None = None,
):
    """
    Returns:
    (cfo_sign, cfi_sign, cff_sign, pattern_label)
    """

    cfo = _cashflow_sign(operating_activity)
    cfi = _cashflow_sign(investing_activity)
    cff = _cashflow_sign(financing_activity)

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):

        if cfo_quality is not None and cfo_quality > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return cfo, cfi, cff, label