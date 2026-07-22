import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.dashboard.utils.db import get_peer_comparison_data

st.title("🤝 Peer Comparison")

df = get_peer_comparison_data()

# -----------------------------
# Peer Group Selection
# -----------------------------
peer_group = st.selectbox(
    "Select Peer Group",
    sorted(df["peer_group_name"].dropna().unique())
)

peer_df = df[df["peer_group_name"] == peer_group]

# -----------------------------
# Company Selection
# -----------------------------
company = st.selectbox(
    "Select Company",
    sorted(peer_df["company_name"].unique())
)

company_df = peer_df[peer_df["company_name"] == company]

st.divider()

st.subheader("📊 Peer Group KPI Comparison")

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr"
]
st.subheader("📋 All Companies in Peer Group")

display_df = peer_df[
    [
        "is_benchmark",
        "company_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
    ]
].copy()

display_df.columns = [
    "Benchmark",
    "Company",
    "ROE",
    "ROCE",
    "NPM",
    "Debt/Equity",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
]

display_df["Benchmark"] = display_df["Benchmark"].apply(
    lambda x: "⭐" if x == 1 else ""
)

st.dataframe(
    display_df.style.apply(
        lambda row: [
            "background-color:#FFF3B0" if row["Benchmark"] == "⭐" else ""
            for _ in row
        ],
        axis=1,
    ),
    use_container_width=True,
    hide_index=True,
)
st.subheader("📈 Radar Comparison")

normalized = peer_df[metrics].copy()

for col in metrics:
    min_val = normalized[col].min()
    max_val = normalized[col].max()

    if max_val != min_val:
        normalized[col] = (
            (normalized[col] - min_val)
            / (max_val - min_val)
        ) * 100
    else:
        normalized[col] = 50

company_values = normalized.loc[
    company_df.index,
    metrics
].iloc[0].tolist()

peer_values = normalized[metrics].mean().tolist()

labels = [
    "ROE",
    "ROCE",
    "NPM",
    "Debt/Equity",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR"
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)