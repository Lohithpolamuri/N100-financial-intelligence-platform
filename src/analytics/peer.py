import sqlite3
import pandas as pd
from pathlib import Path

from src.screener.engine import ScreenerEngine


class PeerAnalytics:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        DB_PATH = BASE_DIR / "db" / "n100.db"

        self.conn = sqlite3.connect(str(DB_PATH))

        # Load latest financial data from Screener Engine
        self.engine = ScreenerEngine()
        self.master_df = self.engine.master_df
        print(self.master_df.columns.tolist())

    def load_data(self):

        peer_groups = pd.read_sql(
            "SELECT * FROM peer_groups",
            self.conn
        )

        merged_df = peer_groups.merge(
            self.master_df,
            on="company_id",
            how="left"
        )

        return merged_df

    def calculate_percentiles(self):

        df = self.load_data().copy()

        metrics = {
            "return_on_equity_pct": False,
            "return_on_capital_employed_pct": False,
            "net_profit_margin_pct": False,
            "debt_to_equity": True,
            "free_cash_flow_cr": False,
            "revenue_cagr_5yr": False,
            "pat_cagr_5yr": False,
            "eps_cagr_5yr": False,
            "interest_coverage": False,
            "asset_turnover": False
        }

        result = []

        for metric, reverse in metrics.items():

            temp = df[
                ["peer_group_name", "company_id", "year", metric]
            ].copy()

            if reverse:
                temp["percentile_rank"] = (
                        temp.groupby("peer_group_name")[metric]
                        .rank(pct=True, ascending=False) * 100
                )
            else:
                temp["percentile_rank"] = (
                        temp.groupby("peer_group_name")[metric]
                        .rank(pct=True, ascending=True) * 100
                )

            temp["metric"] = metric

            temp = temp.rename(columns={metric: "value"})
            print(f"Processing metric: {metric}, Rows: {len(temp)}")

            result.append(temp)

        final_df = pd.concat(result, ignore_index=True)
        print(final_df["metric"].unique())

        return final_df

    def save_to_database(self):

        df = self.calculate_percentiles()

        df.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="replace",
            index=False
        )

        print("=" * 60)
        print("PEER PERCENTILES SAVED")
        print("=" * 60)
        print("Rows :", len(df))

    def get_peer_group(self, company_id):

        peer_groups = pd.read_sql(
            "SELECT * FROM peer_groups",
            self.conn
        )

        row = peer_groups[peer_groups["company_id"] == company_id]

        if row.empty:
            return "No peer group assigned"

        return row.iloc[0]["peer_group_name"]

if __name__ == "__main__":
    analytics = PeerAnalytics()
    analytics.save_to_database()