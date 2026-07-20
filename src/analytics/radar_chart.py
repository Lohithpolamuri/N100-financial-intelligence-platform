import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from src.screener.engine import ScreenerEngine


class RadarCharts:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        self.conn = sqlite3.connect(
            BASE_DIR / "db" / "n100.db"
        )

        self.engine = ScreenerEngine()

        self.df = self.engine.master_df.copy()

        peer_groups = pd.read_sql(
            "SELECT * FROM peer_groups",
            self.conn
        )

        self.df = self.df.merge(
            peer_groups,
            on="company_id",
            how="left"
        )

        self.output_folder = (
            BASE_DIR /
            "reports" /
            "radar_charts"
        )

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "pat_cagr_5yr",
            "revenue_cagr_5yr",
            "composite_quality_score"
        ]

    def get_peer_average(self, peer_group):
        peer_df = self.df[
            self.df["peer_group_name"] == peer_group
            ]

        return peer_df[self.metrics].mean(numeric_only=True)

    def get_company(self, company_id):
        row = self.df[
            self.df["company_id"] == company_id
            ]

        if row.empty:
            return None

        return row.iloc[0]

    def plot_radar(self, company_id):

        company = self.get_company(company_id)

        if company is None:
            return

        peer_group = company["peer_group_name"]

        if pd.isna(peer_group):

            nifty_avg = self.df[self.metrics].mean(numeric_only=True)

            company_values = company[self.metrics].fillna(0).astype(float).tolist()
            peer_values = nifty_avg.fillna(0).astype(float).tolist()

            title = f"{company_id} (Nifty100 Avg)"

        else:

            peer_avg = self.get_peer_average(peer_group)

            company_values = company[self.metrics].fillna(0).astype(float).tolist()
            peer_values = peer_avg.fillna(0).astype(float).tolist()

            title = f"{company_id} ({peer_group})"

        peer_avg = self.get_peer_average(peer_group)

        company_values = company[self.metrics].fillna(0).astype(float).tolist()
        peer_values = peer_avg.fillna(0).astype(float).tolist()

        labels = [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "Revenue CAGR",
            "Composite"
        ]

        company_values += company_values[:1]
        peer_values += peer_values[:1]

        angles = np.linspace(
            0,
            2 * np.pi,
            len(labels),
            endpoint=False
        ).tolist()

        angles += angles[:1]

        fig, ax = plt.subplots(
            figsize=(8, 8),
            subplot_kw=dict(polar=True)
        )

        ax.plot(
            angles,
            company_values,
            linewidth=2,
            label=company_id
        )

        ax.fill(
            angles,
            company_values,
            alpha=0.25
        )

        ax.plot(
            angles,
            peer_values,
            linestyle="--",
            linewidth=2,
            label="Reference"
        )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10)

        ax.set_title(
            title,
            fontsize=14
        )

        ax.legend(
            loc="upper right"
        )

        plt.tight_layout()

        plt.savefig(
            self.output_folder / f"{company_id}_radar.png",
            dpi=300
        )

        plt.close()

    def generate_all(self):
        print("Rows in DataFrame:", len(self.df))
        print("Unique Companies:", self.df["company_id"].nunique())

        for company in self.df["company_id"]:
            self.plot_radar(company)

        print("=" * 60)
        print("RADAR CHARTS GENERATED")
        print("=" * 60)

if __name__ == "__main__":

    charts = RadarCharts()

    charts.generate_all()
