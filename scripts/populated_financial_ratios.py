"""
Sprint 2 - Day 12
Populate financial_ratios table
"""

from pathlib import Path
import sqlite3
from src.analytics.ratios import *
from src.analytics.cagr import *
from src.analytics.cashflow_kpis import *
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"

print("=" * 60)
print("DAY 12 - FINANCIAL RATIO ENGINE")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

# ---------------------------------------------------------
# LOAD TABLES
# ---------------------------------------------------------

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

balancesheet = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

profitloss = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print(f"Companies           : {len(companies)}")
print(f"Balance Sheet       : {len(balancesheet)}")
print(f"Profit & Loss       : {len(profitloss)}")
print(f"Cash Flow           : {len(cashflow)}")
print(f"Financial Ratios    : {len(financial_ratios)}")
# ==========================================================
# MERGE ALL TABLES
# ==========================================================

merged = profitloss.merge(
    balancesheet,
    on=["company_id", "year"],
    how="inner"
)

merged = merged.merge(
    cashflow,
    on=["company_id", "year"],
    how="left"
)

print("-" * 60)
print(f"Merged Records : {len(merged)}")
# ==========================================================
# BUILD RATIO ENGINE
# ==========================================================

ratio_results = []

for _, row in merged.iterrows():
    # ==========================================================
    # PROFITABILITY RATIOS
    # ==========================================================

    npm = net_profit_margin(
        row["net_profit"],
        row["sales"]
    )

    opm = operating_profit_margin(
        row["operating_profit"],
        row["sales"],
        row["opm_percentage"]
    )

    roe = return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    )

    roce = return_on_capital_employed(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    )

    roa = return_on_assets(
        row["net_profit"],
        row["total_assets"]
    )

    # ==========================================================
    # LEVERAGE
    # ==========================================================

    de = debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    )

    icr = interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    )

    asset = asset_turnover(
        row["sales"],
        row["total_assets"]
    )

    # ==========================================================
    # CASH FLOW
    # ==========================================================

    fcf = free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    )

    capex_value, capex_label = capex_intensity(
        row["investing_activity"],
        row["sales"]
    )

    ratio_results.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "net_profit_margin_pct": npm,
        "operating_profit_margin_pct": opm,
        "return_on_equity_pct": roe,
        "debt_to_equity": de,
        "interest_coverage": icr,
        "asset_turnover": asset,
        "free_cash_flow_cr": fcf,
        "capex_cr": capex_value,
        "earnings_per_share": row["eps"],
        "book_value_per_share":
            round(
                (row["equity_capital"] + row["reserves"])
                / row["equity_capital"],
                2
            ) if row["equity_capital"] != 0 else None,
        "dividend_payout_ratio_pct":
            row["dividend_payout"],
        "total_debt_cr":
            row["borrowings"],
        "cash_from_operations_cr":
            row["operating_activity"]
    })

print(f"Rows Ready : {len(ratio_results)}")
ratio_df = pd.DataFrame(ratio_results)

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()

print(f"Financial Ratios Saved : {len(ratio_df)}")

conn.close()
print(merged.columns.tolist())