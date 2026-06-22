from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

# =========================
# COMPANIES
# =========================

companies = pd.read_csv(
    BASE_DIR / "data" / "processed" / "companies_clean.csv",
    skiprows=1
)

companies = companies.rename(columns={
    "id": "company_id"
})

companies = companies[
    [
        "company_id",
        "company_name"
    ]
]

companies.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

print("Companies Loaded Successfully")

# =========================
# BALANCESHEET
# =========================

balancesheet = pd.read_csv(
    BASE_DIR / "data" / "processed" / "balancesheet_clean.csv",
    skiprows=1
)

print("BalanceSheet Columns:")
print(balancesheet.columns)

balancesheet = balancesheet.rename(columns={
    "company": "company_id",
    "total_asset": "total_assets"
})

balancesheet = balancesheet[
    [
        "company_id",
        "year",
        "total_assets",
        "total_liabilities"
    ]
]

balancesheet.to_sql(
    "balancesheet",
    conn,
    if_exists="replace",
    index=False
)

print("Balance Sheet Loaded Successfully")

# =========================
# PROFIT AND LOSS
# =========================

profitloss = pd.read_csv(
    BASE_DIR / "data" / "processed" / "profitandloss_clean.csv",

)

print("ProfitLoss Columns:")
print(profitloss.columns)

profitloss = profitloss.rename(columns={
    "company": "company_id",
    "sale": "sales",
    "net_prof": "net_profit"
})

profitloss = profitloss[
    [
        "company_id",
        "year",
        "sales",
        "net_profit"
    ]
]

profitloss.to_sql(
    "profitandloss",
    conn,
    if_exists="replace",
    index=False
)

print("Profit & Loss Loaded Successfully")

conn.commit()
conn.close()

print("All Data Loaded Successfully")