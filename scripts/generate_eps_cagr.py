from pathlib import Path
import sqlite3
import pandas as pd

from src.analytics.cagr import eps_cagr_5yr

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

profitloss = pd.read_sql(
    """
    SELECT company_id, year, eps
    FROM profitandloss
    """,
    conn
)

# Remove TTM
profitloss = profitloss[
    profitloss["year"] != "TTM"
]

results = []

companies = pd.read_sql(
    "SELECT company_id FROM companies",
    conn
)

profitloss = profitloss[
    profitloss["company_id"].isin(
        companies["company_id"]
    )
]

for company in companies["company_id"]:


    company_df = (
        profitloss[
            profitloss["company_id"] == company
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    if len(company_df) < 6:
        continue

    start_eps = company_df.iloc[-6]["eps"]
    end_eps = company_df.iloc[-1]["eps"]

    value, flag = eps_cagr_5yr(
        start_eps,
        end_eps
    )

    results.append({
        "company_id": company,
        "eps_cagr_5yr": value,
        "flag": flag
    })

eps_df = pd.DataFrame(results)

# ==========================================================
# SAVE TO SQLITE
# ==========================================================

eps_df.to_sql(
    "eps_cagr",
    conn,
    if_exists="replace",
    index=False
)

print("=" * 60)
print("EPS CAGR GENERATED")
print("=" * 60)

print(eps_df.head())

print()

print("Companies :", len(eps_df))

print()

print("Saved table : eps_cagr")

conn.close()