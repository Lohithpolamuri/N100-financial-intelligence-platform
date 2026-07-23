import pandas as pd
import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parents[2] / "db" / "n100.db"


def load_valuation_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.company_id,
        c.company_name,

        s.broad_sector,

        fr.year,
        fr.free_cash_flow_cr,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda

    FROM companies c

    JOIN financial_ratios fr
        ON c.company_id = fr.company_id

    JOIN market_cap mc
        ON c.company_id = mc.company_id
        AND CAST(REPLACE(fr.year,'Mar ','') AS INTEGER)=mc.year

    JOIN sectors s
        ON c.company_id=s.company_id

    ORDER BY
        c.company_name,
        fr.year
    """

    df = pd.read_sql(query, conn)

    # Remove duplicate company-year records
    df = df.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    conn.close()

    return df
if __name__ == "__main__":

    df = load_valuation_data()
    # Calculate FCF Yield (%)
    df["fcf_yield_pct"] = (
                                  df["free_cash_flow_cr"] / df["market_cap_crore"]
                          ) * 100

    latest_df = df[df["year"] == "Mar 2024"]

    sector_pe = (
        latest_df.groupby("broad_sector")["pe_ratio"]
        .median()
        .reset_index()
        .rename(columns={"pe_ratio": "sector_median_pe"})
    )

    df = df.merge(
        sector_pe,
        on="broad_sector",
        how="left"
    )
    # Calculate 5-Year Median PE for each company
    company_5yr_pe = (
        df.groupby("company_id")["pe_ratio"]
        .median()
        .reset_index()
        .rename(columns={"pe_ratio": "5yr_median_PE"})
    )

    df = df.merge(
        company_5yr_pe,
        on="company_id",
        how="left"
    )
    # Calculate PE vs Sector Median (%)
    df["PE_vs_sector_median_pct"] = (
                                            (df["pe_ratio"] - df["sector_median_pe"])
                                            / df["sector_median_pe"]
                                    ) * 100


    # Create Valuation Flag

    # Default flag
    df["flag"] = "Fair"

    # Caution: PE > 1.5 × Sector Median
    df.loc[
        df["pe_ratio"] > (df["sector_median_pe"] * 1.5),
        "flag"
    ] = "Caution"

    # Discount: PE < 0.7 × Sector Median
    df.loc[
        df["pe_ratio"] < (df["sector_median_pe"] * 0.7),
        "flag"
    ] = "Discount"


    # Create valuation summary
    summary = df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "year",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "fcf_yield_pct",
            "5yr_median_PE",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ]

    # Export Excel
    from pathlib import Path

    OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    summary.to_excel(
        OUTPUT_DIR / "valuation_summary.xlsx",
        index=False
    )
    flagged = df[
        df["flag"].isin(["Caution", "Discount"])
    ]

    flagged.to_csv(
        OUTPUT_DIR / "valuation_flags.csv",
        index=False
    )

    print("\n✅ valuation_summary.xlsx created")
    print("✅ valuation_flags.csv created")

