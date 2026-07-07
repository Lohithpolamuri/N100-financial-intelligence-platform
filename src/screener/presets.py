"""
Sprint 3 - Day 16
Preset Screeners

Author: Lohith
"""

import pandas as pd


class PresetScreeners:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    # ==========================================================
    # QUALITY COMPOUNDER
    # ==========================================================

    def quality_compounder(self):

        df = self.df.copy()

        df = df[
            (df["return_on_equity_pct"] > 15)
            &
            (df["debt_to_equity"] < 1)
            &
            (df["free_cash_flow_cr"] > 0)
            &
            (df["compounded_sales_growth"] > 10)
        ]

        return df.sort_values(
            "return_on_equity_pct",
            ascending=False
        )

    # ==========================================================
    # VALUE PICK
    # ==========================================================

    def value_pick(self):
        df = self.df.copy()

        df = df[
            (df["pe_ratio"] < 20)
            &
            (df["pb_ratio"] < 3)
            &
            (df["debt_to_equity"] < 2)
            &
            (df["dividend_yield_pct"] > 1)
            ]

        return df.sort_values(
            "dividend_yield_pct",
            ascending=False
        )

    # ==========================================================
    # GROWTH ACCELERATOR
    # ==========================================================

    def growth_accelerator(self):
        df = self.df.copy()
        print("\nGrowth Data Preview")
        print(
            df[
                [
                    "company_id",
                    "compounded_sales_growth",
                    "compounded_profit_growth",
                    "debt_to_equity"
                ]
            ].head(20)
        )
        print("\nRevenue CAGR > 15 :", (df["compounded_sales_growth"] > 15).sum())
        print("PAT CAGR > 20 :", (df["compounded_profit_growth"] > 20).sum())
        print("D/E < 2 :", (df["debt_to_equity"] < 2).sum())
        print(df[
                  [
                      "company_id",
                      "compounded_sales_growth",
                      "compounded_profit_growth"
                  ]
              ].dropna().head(20))

        df = df[
            (df["compounded_profit_growth"] > 20)
            &
            (df["compounded_sales_growth"] > 15)
            &
            (df["debt_to_equity"] < 2)
            ]

        return df.sort_values(
            "compounded_profit_growth",
            ascending=False
        )

    # ==========================================================
    # DIVIDEND CHAMPION
    # ==========================================================

    def dividend_champion(self):
        df = self.df.copy()

        df = df[
            (df["dividend_yield_pct"] > 3)
            &
            (df["dividend_payout_ratio_pct"] > 0)
            &
            (df["dividend_payout_ratio_pct"] < 60)
            &
            (df["free_cash_flow_cr"] > 0)
            ]

        return df.sort_values(
            "dividend_yield_pct",
            ascending=False
        )

    # ==========================================================
    # DEBT-FREE BLUE CHIP
    # ==========================================================

    def debt_free_blue_chip(self):
        df = self.df.copy()

        df = df[
            (df["debt_to_equity"] == 0)
            &
            (df["return_on_equity_pct"] > 12)
            &
            (df["sales"] > 5000)
            ]

        return df.sort_values(
            "return_on_equity_pct",
            ascending=False
        )

    # ==========================================================
    # TURNAROUND WATCH
    # ==========================================================

    def turnaround_watch(self):
        df = self.df.copy()

        df = df[
            (df["free_cash_flow_cr"] > 0)
            &
            (df["debt_to_equity"] < 1)
            &
            (df["compounded_sales_growth"] > 10)
            ]

        return df.sort_values(
            "free_cash_flow_cr",
            ascending=False
        )