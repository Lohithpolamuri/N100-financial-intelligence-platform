"""
Sprint 3
Build CAGR Metrics Table

Author: Lohith
"""

from pathlib import Path
import sqlite3
import pandas as pd

from src.analytics.cagr import (
    revenue_cagr_3yr,
    revenue_cagr_5yr,
    revenue_cagr_10yr,
    pat_cagr_3yr,
    pat_cagr_5yr,
    pat_cagr_10yr,
    eps_cagr_3yr,
    eps_cagr_5yr,
    eps_cagr_10yr,
)

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)
profitloss = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        eps
    FROM profitandloss
    """,
    conn
)
profitloss = profitloss[
    profitloss["year"] != "TTM"
]
profitloss["year_num"] = (
    profitloss["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

profitloss = profitloss.sort_values(
    ["company_id", "year_num"]
)
companies = pd.read_sql(
    "SELECT company_id FROM companies",
    conn
)
results = []
for company in companies["company_id"]:

    company_df = (
        profitloss[
            profitloss["company_id"] == company
        ]
        .copy()
        .sort_values("year_num")
        .reset_index(drop=True)
    )

    latest = company_df.iloc[-1]

    # ==========================================================
    # REVENUE CAGR
    # ==========================================================

    rev3 = rev5 = rev10 = None

    if len(company_df) >= 4:
        rev3, _ = revenue_cagr_3yr(
            company_df.iloc[-4]["sales"],
            latest["sales"]
        )

    if len(company_df) >= 6:
        rev5, _ = revenue_cagr_5yr(
            company_df.iloc[-6]["sales"],
            latest["sales"]
        )

    if len(company_df) >= 11:
        rev10, _ = revenue_cagr_10yr(
            company_df.iloc[-11]["sales"],
            latest["sales"]
        )

    # ==========================================================
    # PAT CAGR
    # ==========================================================

    pat3 = pat5 = pat10 = None

    if len(company_df) >= 4:
        pat3, _ = pat_cagr_3yr(
            company_df.iloc[-4]["net_profit"],
            latest["net_profit"]
        )

    if len(company_df) >= 6:
        pat5, _ = pat_cagr_5yr(
            company_df.iloc[-6]["net_profit"],
            latest["net_profit"]
        )

    if len(company_df) >= 11:
        pat10, _ = pat_cagr_10yr(
            company_df.iloc[-11]["net_profit"],
            latest["net_profit"]
        )

    # ==========================================================
    # EPS CAGR
    # ==========================================================

    eps3 = eps5 = eps10 = None

    if len(company_df) >= 4:
        eps3, _ = eps_cagr_3yr(
            company_df.iloc[-4]["eps"],
            latest["eps"]
        )

    if len(company_df) >= 6:
        eps5, _ = eps_cagr_5yr(
            company_df.iloc[-6]["eps"],
            latest["eps"]
        )

    if len(company_df) >= 11:
        eps10, _ = eps_cagr_10yr(
            company_df.iloc[-11]["eps"],
            latest["eps"]
        )
    results.append({

        "company_id": company,

        "revenue_cagr_3yr": rev3,
        "revenue_cagr_5yr": rev5,
        "revenue_cagr_10yr": rev10,

        "pat_cagr_3yr": pat3,
        "pat_cagr_5yr": pat5,
        "pat_cagr_10yr": pat10,

        "eps_cagr_3yr": eps3,
        "eps_cagr_5yr": eps5,
        "eps_cagr_10yr": eps10

    })
    cagr_df = pd.DataFrame(results)

    print(cagr_df.head())

    print()
    print("Companies :", len(cagr_df))
# ==========================================================
# SAVE TO SQLITE
# ==========================================================

cagr_df.to_sql(
    "cagr_metrics",
    conn,
    if_exists="replace",
    index=False
)

print("\nCAGR table saved successfully.")

conn.close()