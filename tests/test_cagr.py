from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr_3yr,
    revenue_cagr_5yr,
    revenue_cagr_10yr,
    pat_cagr_3yr,
    eps_cagr_3yr,
    NORMAL,
    DECLINE_TO_LOSS,
    TURNAROUND,
    BOTH_NEGATIVE,
    ZERO_BASE,
    INSUFFICIENT,
)


# 1. Normal CAGR
def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)
    assert value is not None
    assert flag == NORMAL


# 2. Positive -> Negative
def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5)
    assert value is None
    assert flag == DECLINE_TO_LOSS


# 3. Negative -> Positive
def test_turnaround():
    value, flag = calculate_cagr(-100, 50, 5)
    assert value is None
    assert flag == TURNAROUND


# 4. Negative -> Negative
def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)
    assert value is None
    assert flag == BOTH_NEGATIVE


# 5. Zero Base
def test_zero_base():
    value, flag = calculate_cagr(0, 100, 5)
    assert value is None
    assert flag == ZERO_BASE


# 6. Insufficient Years
def test_insufficient():
    value, flag = calculate_cagr(100, 200, 0)
    assert value is None
    assert flag == INSUFFICIENT


# 7. Revenue CAGR
def test_revenue_cagr():
    value, flag = revenue_cagr_3yr(100, 150)
    assert flag == NORMAL


# 8. Revenue CAGR 5 Year
def test_revenue_cagr_5yr():
    value, flag = revenue_cagr_5yr(100, 200)
    assert flag == NORMAL


# 9. Revenue CAGR 10 Year
def test_revenue_cagr_10yr():
    value, flag = revenue_cagr_10yr(100, 300)
    assert flag == NORMAL


# 10. PAT & EPS CAGR
def test_pat_eps_cagr():
    p, pf = pat_cagr_3yr(100, 200)
    e, ef = eps_cagr_3yr(10, 20)

    assert pf == NORMAL
    assert ef == NORMAL