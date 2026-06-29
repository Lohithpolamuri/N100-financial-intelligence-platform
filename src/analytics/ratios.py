"""
Sprint 2 - Day 08
Profitability Ratio Engine
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = Net Profit / Sales × 100
    """
    if sales == 0:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales, expected_opm=None):
    """
    Operating Profit Margin = Operating Profit / Sales × 100
    Cross-check with existing OPM value.
    """

    if sales == 0:
        return None

    opm = round((operating_profit / sales) * 100, 2)

    if expected_opm is not None:
        if abs(opm - expected_opm) > 1:
            logger.warning(
                f"OPM mismatch detected. Calculated={opm}, Existing={expected_opm}"
            )

    return opm


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity Capital + Reserves) × 100
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
    broad_sector=None
):
    """
    ROCE = EBIT / (Equity + Reserves + Borrowings) × 100

    Financial sector companies are flagged differently.
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    roce = round((ebit / capital) * 100, 2)

    if broad_sector is not None:
        if broad_sector.lower() == "financials":
            logger.info(
                "Financial sector company detected. "
                "Use sector-relative benchmark."
            )

    return roce


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets × 100
    """

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)