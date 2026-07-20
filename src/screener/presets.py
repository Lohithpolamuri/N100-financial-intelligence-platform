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
            (df["revenue_cagr_5yr"] > 10)
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

        print("Total Companies :", len(df))

        temp = df[df["pe_ratio"] < 20]
        print("After PE :", len(temp))

        temp = temp[temp["pb_ratio"] < 3]
        print("After PB :", len(temp))

        temp = temp[temp["debt_to_equity"] < 2]
        print("After Debt/Equity :", len(temp))

        temp = temp[temp["dividend_yield_pct"] > 1]
        print("After Dividend Yield :", len(temp))

        print(
            temp[
                [
                    "company_id",
                    "pe_ratio",
                    "pb_ratio",
                    "debt_to_equity",
                    "dividend_yield_pct"
                ]
            ]
        )

        return temp.sort_values(
            "dividend_yield_pct",
            ascending=False
        )

    # ==========================================================
    # GROWTH ACCELERATOR
    # ==========================================================

    def growth_accelerator(self):
        df = self.df.copy()

        df = df[
            (df["revenue_cagr_5yr"] > 15)
            &
            (df["pat_cagr_5yr"] > 20)
            &
            (df["debt_to_equity"] < 2)
            ]

        return df.sort_values(
            "revenue_cagr_5yr",
            ascending=False
        )

    # ==========================================================
    # DIVIDEND CHAMPION
    # ==========================================================

    def dividend_champion(self):
        df = self.df.copy()

        df = df[
            (df["dividend_yield_pct"] > 2)
            &
            (df["dividend_payout_ratio_pct"] < 80)
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

    def debt_free_bluechip(self):
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
            (df["revenue_cagr_3yr"] > 10)
            ]

        return df.sort_values(
            "free_cash_flow_cr",
            ascending=False
        )