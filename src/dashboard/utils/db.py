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
@st.cache_data(ttl=600)
def get_screener_data():

    conn = get_connection()

    query = """
    SELECT
        c.company_id,
        c.company_name,

        s.broad_sector,

        COALESCE(ROUND(AVG(pp.percentile_rank),2), 0) AS composite_score,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.operating_profit_margin_pct,
        fr.interest_coverage,

        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct,

        cg.revenue_cagr_5yr,
        cg.pat_cagr_5yr

    FROM companies c

    LEFT JOIN sectors s
        ON c.company_id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.company_id = fr.company_id

    LEFT JOIN market_cap mc
        ON c.company_id = mc.company_id

    LEFT JOIN cagr_metrics cg
        ON c.company_id = cg.company_id

    LEFT JOIN peer_percentiles pp
        ON c.company_id = pp.company_id

    WHERE fr.year='Mar 2024'
      AND mc.year=2024

    GROUP BY c.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_comparison_data():
    conn = get_connection()

    query = """
    SELECT
    pg.peer_group_name,
    pg.is_benchmark,

    c.company_name,
    c.company_id,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,

        cg.revenue_cagr_5yr,
        cg.pat_cagr_5yr

    FROM peer_groups pg

    JOIN companies c
        ON pg.company_id = c.company_id

    LEFT JOIN financial_ratios fr
        ON c.company_id = fr.company_id

    LEFT JOIN cagr_metrics cg
        ON c.company_id = cg.company_id

    WHERE fr.year='Mar 2024'
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df
@st.cache_data(ttl=600)
def get_trend_data():
    conn = get_connection()

    query = """
    SELECT
        c.company_id,
        c.company_name,

        fr.year,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.free_cash_flow_cr

    FROM financial_ratios fr

    JOIN companies c
        ON fr.company_id = c.company_id

    WHERE fr.year LIKE 'Mar%'

    ORDER BY
        c.company_name,
        fr.year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_sector_analysis_data():
    conn = get_connection()

    query = """
    SELECT

        c.company_id,
        c.company_name,

        s.broad_sector,
        s.sub_sector,

        p.sales,

        fr.return_on_equity_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,

        mc.market_cap_crore

    FROM companies c

    JOIN sectors s
        ON c.company_id = s.company_id

    LEFT JOIN profitandloss p
        ON c.company_id = p.company_id

    LEFT JOIN financial_ratios fr
        ON c.company_id = fr.company_id

    LEFT JOIN market_cap mc
        ON c.company_id = mc.company_id

    WHERE
        p.year='Mar 2024'
        AND fr.year='Mar 2024'
        AND mc.year=2024

    ORDER BY
        s.broad_sector,
        c.company_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_capital_allocation_data():

    # Read generated capital allocation file
    allocation = pd.read_csv("output/capital_allocation.csv")

    conn = get_connection()

    companies = pd.read_sql("""
        SELECT company_id, company_name
        FROM companies
    """, conn)

    conn.close()

    # Keep latest record for each company
    allocation = allocation.sort_values("year")

    allocation = allocation.drop_duplicates(
        subset="company_id",
        keep="last"
    )

    # Merge company names
    df = allocation.merge(
        companies,
        on="company_id",
        how="left"
    )
    st.write(df.columns)

    return df
@st.cache_data(ttl=600)
def get_annual_reports():

    reports = pd.read_excel(
        "data/raw/documents.xlsx",
        header=1
    )

    conn = get_connection()

    companies = pd.read_sql("""
        SELECT company_id, company_name
        FROM companies
    """, conn)

    conn.close()

    reports["company_id"] = reports["company_id"].astype(str).str.strip()
    companies["company_id"] = companies["company_id"].astype(str).str.strip()

    df = reports.merge(
        companies,
        on="company_id",
        how="left"
    )

    return df
