import numpy as np
import pandas as pd


class CompositeScore:

    def __init__(self, df):
        self.df = df.copy()

    def normalize(self, column, reverse=False):
        """
        Normalize using P10/P90 Winsorization.
        """

        values = pd.to_numeric(
            self.df[column],
            errors="coerce"
        )

        p10 = values.quantile(0.10)
        p90 = values.quantile(0.90)

        # Cap extreme values
        values = values.clip(
            lower=p10,
            upper=p90
        )

        if p10 == p90:
            score = pd.Series(
                50,
                index=self.df.index,
                dtype=float
            )
        else:
            score = (
                            (values - p10)
                            / (p90 - p10)
                    ) * 100

        if reverse:
            score = 100 - score

        return score.fillna(0)

    def calculate(self):

        df = self.df

        # Profitability (40%)

        roe = self.normalize(
            "return_on_equity_pct"
        )

        npm = self.normalize(
            "net_profit_margin_pct"
        )

        opm = self.normalize(
            "operating_profit_margin_pct"
        )

        # Cash Quality (25%)

        fcf = self.normalize(
            "free_cash_flow_cr"
        )

        cfo = self.normalize(
            "cash_from_operations_cr"
        )

        # Growth (20%)

        rev = self.normalize(
            "revenue_cagr_5yr"
        )

        pat = self.normalize(
            "pat_cagr_5yr"
        )

        # Leverage (15%)

        debt = self.normalize(
            "debt_to_equity",
            reverse=True
        )

        icr = self.normalize(
            "interest_coverage"
        )

        # Global Composite Score
        df["composite_quality_score"] = (

                roe * 0.15 +
                npm * 0.15 +
                opm * 0.10 +
                fcf * 0.15 +
                cfo * 0.10 +
                rev * 0.10 +
                pat * 0.10 +
                debt * 0.10 +
                icr * 0.05

        )

        # ==========================================================
        # Sector Relative Composite Score
        # ==========================================================

        df["sector_composite_score"] = (
            df.groupby("broad_sector")["composite_quality_score"]
            .transform(
                lambda x: (
                                  (x - x.min()) /
                                  (x.max() - x.min())
                          ) * 100
                if x.max() != x.min()
                else 50
            )
        )

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )