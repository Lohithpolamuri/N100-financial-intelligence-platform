"""
Sprint 3 - Day 15
Financial Screener Engine
"""
from src.analytics.composite_score import CompositeScore
from pathlib import Path
import sqlite3
import pandas as pd
import yaml
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "db" / "n100.db"


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        self.sectors = pd.read_sql(
            "SELECT company_id, broad_sector FROM sectors",
            self.conn
        )
        self.market_cap = pd.read_sql(
            "SELECT company_id, year, market_cap_crore, pe_ratio, pb_ratio, dividend_yield_pct FROM market_cap",
            self.conn
        )
        self.market_cap["year"] = "Mar " + self.market_cap["year"].astype(str)

        self.cagr_metrics = pd.read_sql(
            """
            SELECT *
            FROM cagr_metrics
            """,
            self.conn
        )
        print("\nCAGR Metrics")
        print(self.cagr_metrics.head())
        print(f"Rows : {len(self.cagr_metrics)}")

        self.profitloss = pd.read_sql(
            "SELECT company_id, year, sales, net_profit FROM profitandloss",
            self.conn
        )

        CONFIG_PATH = BASE_DIR / "config" / "screener_config.yaml"

        with open(CONFIG_PATH, "r") as file:
            self.config = yaml.safe_load(file)

        print("=" * 60)
        print("SPRINT 3 - DAY 15")
        print("=" * 60)
        print(f"Financial Ratio Rows : {len(self.df)}")

        print("\nLoaded Filters")
        print("-" * 60)

        for key, value in self.config["filters"].items():
            print(f"{key:<30} : {value}")

        # Store full merged dataset
        self.master_df = self.prepare_master_dataframe()
        # Calculate Composite Score
        scorer = CompositeScore(self.master_df)
        self.master_df = scorer.calculate()

        # Apply Day 15 filters
        self.filtered_df = self.apply_filters(self.master_df.copy())


    def prepare_master_dataframe(self):
        df = self.df.copy()

        df = df.merge(
            self.market_cap,
            on=["company_id", "year"],
            how="left"
        )

        df = df.merge(
            self.cagr_metrics,
            on="company_id",
            how="left"
        )

        df = df.merge(
            self.profitloss,
            on=["company_id", "year"],
            how="left"
        )

        df = df.merge(
            self.sectors,
            on="company_id",
            how="left"
        )

        # Keep only latest year
        df["year_num"] = (
            df["year"]
            .str.extract(r"(\d{4})")
            .astype(int)
        )

        df = (
            df.sort_values("year_num")
            .groupby("company_id", as_index=False)
            .tail(1)
        )

        df = df.drop(columns="year_num")

        return df



    def apply_filters(self, df):

        filters = self.config["filters"]




        df = df[
            df["return_on_equity_pct"] >= filters["roe_min"]
        ]

        df = df[
            (df["broad_sector"] == "Financials") |
            (df["debt_to_equity"] <= filters["debt_to_equity_max"])
            ]

        df = df[
            df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]

        df = df[
            df["asset_turnover"] >= filters["asset_turnover_min"]
        ]
        # ==========================================================
        # ADDITIONAL FILTERS
        # ==========================================================

        df = df[
            df["sales"] >= filters["sales_min"]
            ]
        print("After Sales :", len(df))


        print("After Net Profit :", len(df))


        print("After Market Cap :", len(df))


        print("After PE :", len(df))



        print("After PB :", len(df))


        print("After Dividend Yield :", len(df))


        # ==========================================================
        # REVENUE CAGR FILTER
        # Skip companies where CAGR data is unavailable
        # ==========================================================

        df = df[
            (
                df["revenue_cagr_5yr"].isna()
            )
            |
            (
                    df["revenue_cagr_5yr"]
                    >= filters["revenue_cagr_5yr_min"]
            )
            ]

        # ==========================================================
        # PAT CAGR FILTER
        # ==========================================================

        df = df[
            (
                df["pat_cagr_5yr"].isna()
            )
            |
            (
                    df["pat_cagr_5yr"]
                    >= filters["pat_cagr_5yr_min"]
            )
            ]
        print(df[
                  ["company_id", "eps_cagr_5yr"]
              ].head(10))
        # ==========================================================
        # EPS CAGR FILTER
        # ==========================================================

        df = df[
            (
                df["eps_cagr_5yr"].isna()
            )
            |
            (
                    df["eps_cagr_5yr"]
                    >= filters["eps_cagr_min"]
            )
            ]

        print("After EPS CAGR :", len(df))




        # ==========================================================
        # INTEREST COVERAGE FILTER
        # Debt Free companies always pass
        # ==========================================================

        icr = pd.to_numeric(
            df["interest_coverage"],
            errors="coerce"
        )

        df = df[
            (
                    icr >= filters["interest_coverage_min"]
            )
            |
            (
                    df["interest_coverage"].astype(str)
                    == "Debt Free"
            )
            ]

        print("\n" + "=" * 60)
        print("FILTER RESULTS")
        print("=" * 60)
        print(f"Companies after filtering : {len(df)}")
        # ==========================================================
        # PLACEHOLDER COMPOSITE SCORE
        # ==========================================================

        df["composite_quality_score"] = 0

        df = df.sort_values(
            by="composite_quality_score",
            ascending=False
        )

        print("\nComposite Score column added.")
        return df



if __name__ == "__main__":

    engine = ScreenerEngine()


    from src.screener.presets import PresetScreeners

    presets = PresetScreeners(
        engine.master_df
    )

    print("\n")
    print("=" * 60)
    print("TOP COMPOSITE SCORES")
    print("=" * 60)

    print(
        engine.master_df[
            [
                "company_id",
                "composite_quality_score"
            ]
        ].head(20)
    )