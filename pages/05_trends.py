import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.dashboard.utils.db import get_trend_data

st.title("📈 Trend Analysis")

df = get_trend_data()

# -------------------------
# Company Selection
# -------------------------

company = st.selectbox(
    "Select Company",
    sorted(df["company_name"].unique())

)

company_df = df[df["company_name"] == company].copy()

# -------------------------
# Metric Selection
# -------------------------

metric_options = {
    "ROE": "return_on_equity_pct",
    "ROCE": "return_on_capital_employed_pct",
    "Net Profit Margin": "net_profit_margin_pct",
    "Operating Profit Margin": "operating_profit_margin_pct",
    "Debt / Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Free Cash Flow": "free_cash_flow_cr",
}

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    list(metric_options.keys()),
    default=["ROE"],
    max_selections=3
)
annotate_metric = st.selectbox(
    "Show YoY annotations for",
    selected_metrics
)

st.divider()
fig = go.Figure()

for metric in selected_metrics:

    column = metric_options[metric]

    temp = company_df.copy()

    temp[column] = temp[column].astype(float)

    temp["YoY"] = temp[column].pct_change() * 100

    # Show text only for the selected annotation metric
    if metric == annotate_metric:
        labels = [
            "" if pd.isna(x) else f"{x:+.0f}%"
            for x in temp["YoY"]
        ]
    else:
        labels = None

    fig.add_trace(
        go.Scatter(
            x=temp["year"],
            y=temp[column],
            mode="lines+markers+text",
            name=metric,
            text=labels,
            textposition="top center"
        )
    )

fig.update_layout(
    title=f"{company} - Financial Trends",
    xaxis_title="Year",
    yaxis_title="Value",
    hovermode="x unified",
    height=650
)

st.plotly_chart(fig, use_container_width=True)