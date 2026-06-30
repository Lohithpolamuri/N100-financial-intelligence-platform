"""
Sprint 2 - Day 10
CAGR Engine

Author: Lohith
"""

from typing import Tuple


# ==========================================================
# CAGR FLAGS
# ==========================================================

NORMAL = "NORMAL"
DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> Tuple[float | None, str]:
    """
    Generic CAGR calculator.

    Formula:
        ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        (value, flag)
    """

    # -----------------------------
    # Not enough years
    # -----------------------------

    if years <= 0:
        return None, INSUFFICIENT

    # -----------------------------
    # Zero base
    # -----------------------------

    if start_value == 0:
        return None, ZERO_BASE

    # -----------------------------
    # Positive → Negative
    # -----------------------------

    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    # -----------------------------
    # Negative → Positive
    # -----------------------------

    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    # -----------------------------
    # Negative → Negative
    # -----------------------------

    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    # -----------------------------
    # Normal CAGR
    # -----------------------------

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), NORMAL
# ==========================================================
# REVENUE CAGR
# ==========================================================

def revenue_cagr(start_sales, end_sales, years):
    """
    Revenue CAGR
    """
    return calculate_cagr(
        start_sales,
        end_sales,
        years
    )


# ==========================================================
# PAT CAGR
# ==========================================================

def pat_cagr(start_profit, end_profit, years):
    """
    PAT CAGR
    """
    return calculate_cagr(
        start_profit,
        end_profit,
        years
    )


# ==========================================================
# EPS CAGR
# ==========================================================

def eps_cagr(start_eps, end_eps, years):
    """
    EPS CAGR
    """
    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )


# ==========================================================
# 3 YEAR
# ==========================================================

def revenue_cagr_3yr(start_sales, end_sales):
    return revenue_cagr(start_sales, end_sales, 3)


def pat_cagr_3yr(start_profit, end_profit):
    return pat_cagr(start_profit, end_profit, 3)


def eps_cagr_3yr(start_eps, end_eps):
    return eps_cagr(start_eps, end_eps, 3)


# ==========================================================
# 5 YEAR
# ==========================================================

def revenue_cagr_5yr(start_sales, end_sales):
    return revenue_cagr(start_sales, end_sales, 5)


def pat_cagr_5yr(start_profit, end_profit):
    return pat_cagr(start_profit, end_profit, 5)


def eps_cagr_5yr(start_eps, end_eps):
    return eps_cagr(start_eps, end_eps, 5)


# ==========================================================
# 10 YEAR
# ==========================================================

def revenue_cagr_10yr(start_sales, end_sales):
    return revenue_cagr(start_sales, end_sales, 10)


def pat_cagr_10yr(start_profit, end_profit):
    return pat_cagr(start_profit, end_profit, 10)


def eps_cagr_10yr(start_eps, end_eps):
    return eps_cagr(start_eps, end_eps, 10)