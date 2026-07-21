from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "n100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()

    query = """
    SELECT
        company_id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = get_connection()

    if year is None:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """

        df = pd.read_sql(query, conn, params=[ticker])

    else:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        AND year=?
        """

        df = pd.read_sql(query, conn, params=[ticker, year])

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name=?
    """

    df = pd.read_sql(query, conn, params=[group_name])

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = get_connection()

    query = """
    SELECT *
    FROM market_cap
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_home_metrics(year=None):
    conn = get_connection()

    query = """
    SELECT
        fr.*,
        c.company_name
    FROM financial_ratios fr
    JOIN companies c
        ON fr.company_id = c.company_id
    """

    params = []

    if year is not None:
        query += " WHERE fr.year = ?"
        params.append(f"Mar {year}")

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_sector_count():
    conn = get_connection()

    query = """
    SELECT COUNT(DISTINCT broad_sector) AS sector_count
    FROM sectors
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return int(result.iloc[0]["sector_count"])
@st.cache_data(ttl=600)
def get_avg_roe(year):
    conn = get_connection()

    query = """
    SELECT ROUND(AVG(return_on_equity_pct),2) AS avg_roe
    FROM financial_ratios
    WHERE year = ?
    """

    result = pd.read_sql(query, conn, params=[f"Mar {year}"])

    conn.close()

    value = result.iloc[0]["avg_roe"]

    return 0 if pd.isna(value) else value
@st.cache_data(ttl=600)
def get_median_pe(year):
    conn = get_connection()

    query = """
    SELECT pe_ratio
    FROM market_cap
    WHERE year = ?
      AND pe_ratio IS NOT NULL
    """

    df = pd.read_sql(query, conn, params=[year])

    conn.close()

    if df.empty:
        return 0

    return round(df["pe_ratio"].median(), 2)
@st.cache_data(ttl=600)
def get_company_count():
    conn = get_connection()

    query = """
    SELECT COUNT(*) AS total
    FROM companies
    """

    result = pd.read_sql(query, conn)

    conn.close()

    return int(result.iloc[0]["total"])
@st.cache_data(ttl=600)
def get_sector_distribution():
    conn = get_connection()

    query = """
    SELECT
        broad_sector,
        COUNT(*) AS company_count
    FROM sectors
    GROUP BY broad_sector
    ORDER BY company_count DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_company_profile(company_id, year):
    conn = get_connection()

    query = """
    SELECT
    c.company_name,

    s.broad_sector,
    s.sub_sector,
    s.market_cap_category,
    s.index_weight_pct,

    mc.market_cap_crore,
    mc.pe_ratio,

    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,

    cg.revenue_cagr_5yr

    FROM companies c

    LEFT JOIN sectors s
        ON c.company_id = s.company_id

    LEFT JOIN market_cap mc
        ON c.company_id = mc.company_id
        AND mc.year = ?

    LEFT JOIN financial_ratios fr
        ON c.company_id = fr.company_id
        AND fr.year = ?
        
    LEFT JOIN cagr_metrics cg
    ON c.company_id = cg.company_id

    WHERE c.company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[year, f"Mar {year}", company_id]
    )

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_roe_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        return_on_equity_pct
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_eps_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        earnings_per_share
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_fcf_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        free_cash_flow_cr
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_median_de(year):
    conn = get_connection()

    query = """
    SELECT debt_to_equity
    FROM financial_ratios
    WHERE year = ?
      AND debt_to_equity IS NOT NULL
    """

    df = pd.read_sql(query, conn, params=[f"Mar {year}"])

    conn.close()

    if df.empty:
        return 0

    return round(df["debt_to_equity"].median(), 2)
@st.cache_data(ttl=600)
def get_median_revenue_cagr():
    conn = get_connection()

    query = """
    SELECT revenue_cagr_5yr
    FROM cagr_metrics
    WHERE revenue_cagr_5yr IS NOT NULL
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if df.empty:
        return 0

    return round(df["revenue_cagr_5yr"].median(), 2)
@st.cache_data(ttl=600)
def get_debt_free_count(year):
    conn = get_connection()

    query = """
    SELECT COUNT(*) AS total
    FROM financial_ratios
    WHERE year = ?
      AND debt_to_equity = 0
    """

    result = pd.read_sql(query, conn, params=[f"Mar {year}"])

    conn.close()

    return int(result.iloc[0]["total"])
@st.cache_data(ttl=600)
def get_top_quality_companies(year):
    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        ROUND(AVG(pp.percentile_rank), 2) AS composite_score
    FROM peer_percentiles pp
    JOIN companies c
        ON pp.company_id = c.company_id
    WHERE pp.year = ?
    GROUP BY pp.company_id, c.company_name
    ORDER BY composite_score DESC
    LIMIT 5
    """

    df = pd.read_sql(
        query,
        conn,
        params=[f"Mar {year}"]
    )

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_revenue_profit_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        sales,
        net_profit
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY CAST(SUBSTR(year, -4) AS INTEGER)
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_roe_roce_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY CAST(SUBSTR(year, -4) AS INTEGER)
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df