import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_sector_analysis_data

st.title("🏭 Sector Analysis")

df = get_sector_analysis_data()

# ----------------------------
# Sector Selection
# ----------------------------

sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].unique())
)

sector_df = df[df["broad_sector"] == sector].copy()

st.write(f"Companies in sector: **{len(sector_df)}**")

# ----------------------------
# Bubble Chart
# ----------------------------

fig = px.scatter(
    sector_df,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    size_max=60,
    title=f"{sector} Sector Analysis"
)

fig.update_layout(
    xaxis_title="Revenue (₹ Crore)",
    yaxis_title="ROE (%)",
    height=650
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📊 Sector Median KPIs")
kpi_df = sector_df[[
    "return_on_equity_pct",
    "sales",
    "market_cap_crore"
]]

median_values = sector_df[
[
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity"
]

].median()

bar_df = (
    median_values
    .rename_axis("KPI")
    .reset_index(name="Median")
)
bar_df["KPI"] = [
    "ROE (%)",
    "Net Profit Margin (%)",
    "Debt / Equity"
]

bar_fig = px.bar(
    bar_df,
    x="KPI",
    y="Median",
    text="Median",
    title=f"{sector} Sector Median KPIs"
)

bar_fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

bar_fig.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Median Value"
)

st.plotly_chart(bar_fig, use_container_width=True)