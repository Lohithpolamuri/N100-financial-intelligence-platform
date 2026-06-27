from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"
RAW_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "output"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

print("=" * 60)
print("DAY 5 - FULL DATA LOAD")
print("=" * 60)
# ======================================================
# LOAD COMPANIES
# ======================================================

companies = pd.read_excel(
    RAW_PATH / "companies.xlsx",
    skiprows=1
)

companies = companies.rename(columns={
    "id": "company_id"
})

companies = companies[[
    "company_id",
    "company_name"
]]

companies.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Companies Loaded : {len(companies)}")
# ======================================================
# LOAD BALANCE SHEET
# ======================================================

balancesheet = pd.read_excel(
    RAW_PATH / "balancesheet.xlsx",
    skiprows=1
)

balancesheet = balancesheet.rename(columns={
    "company": "company_id",
    "total_asset": "total_assets"
})

balancesheet = balancesheet[[
    "company_id",
    "year",
    "total_assets",
    "total_liabilities"
]]

balancesheet.to_sql(
    "balancesheet",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Balance Sheet Loaded : {len(balancesheet)}")


# =========================
# LOAD CASH FLOW
# =========================

cashflow = pd.read_excel(
    RAW_PATH / "cashflow.xlsx",
    header=1
)

cashflow = cashflow[
    [
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ]
]

cashflow.to_sql(
    "cashflow",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Cash Flow Loaded : {len(cashflow)}")
# =========================
# LOAD STOCK PRICES
# =========================

stockprices = pd.read_excel(
    RAW_PATH / "stock_prices.xlsx"
)

stockprices = stockprices[
    [
        "company_id",
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "adjusted_close"
    ]
]

stockprices.to_sql(
    "stock_prices",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Stock Prices Loaded : {len(stockprices)}")
# =========================
# LOAD MARKET CAP
# =========================

marketcap = pd.read_excel(
    RAW_PATH / "market_cap.xlsx"
)

marketcap = marketcap[
    [
        "company_id",
        "year",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct"
    ]
]

marketcap.to_sql(
    "market_cap",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Market Cap Loaded : {len(marketcap)}")
# =========================
# LOAD FINANCIAL RATIOS
# =========================

ratios = pd.read_excel(
    RAW_PATH / "financial_ratios.xlsx"
)

ratios = ratios[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr"
    ]
]

ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Financial Ratios Loaded : {len(ratios)}")
# =========================
# LOAD PEER GROUPS
# =========================

peer = pd.read_excel(
    RAW_PATH / "peer_groups.xlsx"
)

peer = peer[
    [
        "peer_group_name",
        "company_id",
        "is_benchmark"
    ]
]

peer.to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Peer Groups Loaded : {len(peer)}")
# =========================
# LOAD ANALYSIS
# =========================

analysis = pd.read_excel(
    RAW_PATH / "analysis.xlsx",
    header=1
)

analysis = analysis[
    [
        "company_id",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]
]

analysis.to_sql(
    "analysis",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Analysis Loaded : {len(analysis)}")
# =========================
# LOAD SECTORS
# =========================

sectors = pd.read_excel(
    RAW_PATH / "sectors.xlsx"
)

sectors = sectors[
    [
        "company_id",
        "broad_sector",
        "sub_sector",
        "index_weight_pct",
        "market_cap_category"
    ]
]

sectors.to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

print(f"✓ Sectors Loaded : {len(sectors)}")
# =========================
# SAVE CHANGES
# =========================

conn.commit()

print("\n==============================")
print("DAY 5 DATA LOAD COMPLETED")
print("==============================")

conn.close()