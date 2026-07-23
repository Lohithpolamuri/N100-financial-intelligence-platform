import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from src.dashboard.utils.db import (
    get_companies,
    get_company_profile,
    get_roe_trend,
    get_eps_trend,
    get_fcf_trend,
get_revenue_profit_trend,
get_roe_roce_trend,
)

st.title("🏢 Company Profile")
selected_year = st.selectbox(
    "Select Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)
companies = get_companies()

search = st.text_input(
    "Search Company Name or Ticker",
    placeholder="e.g. ABB"
)

filtered = companies[
    companies["company_name"].str.contains(search, case=False, na=False) |
    companies["company_id"].str.contains(search, case=False, na=False)
]

if search and filtered.empty:
    st.warning("⚠️ Ticker not found — please try another.")
    st.stop()

selected_company = st.selectbox(
    "Select Company",
    filtered["company_name"] if search else companies["company_name"]
)

selected_company_id = companies.loc[
    companies["company_name"] == selected_company,
    "company_id"
].iloc[0]
profile = get_company_profile(
    selected_company_id,
    selected_year
)
roce = profile.iloc[0]["return_on_capital_employed_pct"]
net_profit_margin = profile.iloc[0]["net_profit_margin_pct"]
de_ratio = profile.iloc[0]["debt_to_equity"]
fcf = profile.iloc[0]["free_cash_flow_cr"]
revenue_cagr = profile.iloc[0]["revenue_cagr_5yr"]
company_name = profile.iloc[0]["company_name"]
sector = profile.iloc[0]["broad_sector"]
sub_sector = profile.iloc[0]["sub_sector"]
market_cap_category = profile.iloc[0]["market_cap_category"]
index_weight = profile.iloc[0]["index_weight_pct"]
market_cap = profile.iloc[0]["market_cap_crore"]
pe_ratio = profile.iloc[0]["pe_ratio"]
roe = profile.iloc[0]["return_on_equity_pct"]
roe_trend = get_roe_trend(selected_company_id)
eps_trend = get_eps_trend(selected_company_id)
fcf_trend = get_fcf_trend(selected_company_id)
revenue_profit_trend = get_revenue_profit_trend(selected_company_id)
roe_roce_trend = get_roe_roce_trend(selected_company_id)
available_years = roe_trend["year"].nunique()

if available_years < 10:
    st.info(
        f"ℹ️ Limited historical data available: {available_years} year(s) of financial data found for this company."
    )

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric(
        "📈 ROE",
        f"{roe:.2f}%"
    )

with col2:
    st.metric(
        "📊 ROCE",
        f"{roce:.2f}%"
    )

with col3:
    st.metric(
        "💰 Net Profit Margin",
        f"{net_profit_margin:.2f}%"
    )

with col4:
    st.metric(
        "🏦 Debt / Equity",
        f"{de_ratio:.2f}"
    )

with col5:
    st.metric(
        "📈 Revenue CAGR (5Y)",
        f"{revenue_cagr:.2f}%"
    )

with col6:
    st.metric(
        "💵 Free Cash Flow",
        f"₹ {fcf:,.2f} Cr"
    )
st.subheader("🏢 Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Ticker:** {selected_company_id}")
    st.write(f"**Sector:** {sector}")

with col2:
    st.write(f"**Sub Sector:** {sub_sector}")
    st.write(f"**Market Cap Category:** {market_cap_category}")
    st.write(f"**Index Weight:** {index_weight:.2f}%")

st.info("About: Company description is not available in the current dataset.")
st.subheader("📈 ROE Trend")

fig = px.line(
    roe_trend,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="Return on Equity Over Time"
)

fig.update_layout(
    height=400,
    xaxis_title="Financial Year",
    yaxis_title="ROE (%)"
)

st.plotly_chart(fig, width="stretch")
st.subheader("💵 EPS Trend")

fig = px.line(
    eps_trend,
    x="year",
    y="earnings_per_share",
    markers=True,
    title="Earnings Per Share Over Time"
)

fig.update_layout(
    height=400,
    xaxis_title="Financial Year",
    yaxis_title="EPS"
)

st.plotly_chart(fig, width="stretch")
st.subheader("💰 Free Cash Flow Trend")

fig = px.line(
    fcf_trend,
    x="year",
    y="free_cash_flow_cr",
    markers=True,
    title="Free Cash Flow Over Time"
)

fig.update_layout(
    height=400,
    xaxis_title="Financial Year",
    yaxis_title="Free Cash Flow (Cr)"
)

st.plotly_chart(fig, width="stretch")
st.subheader("ℹ️ Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Broad Sector:** {sector}")
    st.write(f"**Sub Sector:** {sub_sector}")

with col2:
    st.write(f"**Market Cap Category:** {market_cap_category}")
    st.write(f"**Index Weight:** {index_weight}%")
    st.write(f"**Financial Year:** {selected_year}")
st.subheader("📊 Revenue & Net Profit (All Available Years)")

fig = go.Figure()

fig.add_bar(
    x=revenue_profit_trend["year"],
    y=revenue_profit_trend["sales"],
    name="Revenue"
)

fig.add_bar(
    x=revenue_profit_trend["year"],
    y=revenue_profit_trend["net_profit"],
    name="Net Profit"
)

fig.update_layout(
    barmode="group",
    xaxis_title="Year",
    yaxis_title="Amount (₹ Cr)",
    height=450
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("📈 ROE vs ROCE Trend")

fig = make_subplots(specs=[[{"secondary_y": True}]])

# ROE Line
fig.add_trace(
    go.Scatter(
        x=roe_roce_trend["year"],
        y=roe_roce_trend["return_on_equity_pct"],
        mode="lines+markers",
        name="ROE"
    ),
    secondary_y=False,
)

# ROCE Line
fig.add_trace(
    go.Scatter(
        x=roe_roce_trend["year"],
        y=roe_roce_trend["return_on_capital_employed_pct"],
        mode="lines+markers",
        name="ROCE"
    ),
    secondary_y=True,
)

fig.update_xaxes(title_text="Year")

fig.update_yaxes(
    title_text="ROE (%)",
    secondary_y=False
)

fig.update_yaxes(
    title_text="ROCE (%)",
    secondary_y=True
)

fig.update_layout(
    height=450,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("✅ Pros & ❌ Cons")

pros = []
cons = []

# ROE
if roe >= 15:
    pros.append("Strong Return on Equity")
elif roe < 10:
    cons.append("Low Return on Equity")

# ROCE
if roce >= 15:
    pros.append("Efficient Capital Utilization")
elif roce < 10:
    cons.append("Low Return on Capital Employed")

# Debt
if de_ratio == 0:
    pros.append("Debt-Free Company")
elif de_ratio <= 0.5:
    pros.append("Low Debt")
elif de_ratio > 1:
    cons.append("High Debt Levels")

# Revenue Growth
if revenue_cagr >= 10:
    pros.append("Healthy Revenue Growth (5Y)")
elif revenue_cagr < 5:
    cons.append("Weak Revenue Growth")

# Free Cash Flow
if fcf > 0:
    pros.append("Positive Free Cash Flow")
else:
    cons.append("Negative Free Cash Flow")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Pros")
    if pros:
        for item in pros:
            st.success(item)
    else:
        st.info("No major strengths identified.")

with col2:
    st.markdown("### ❌ Cons")
    if cons:
        for item in cons:
            st.error(item)
    else:
        st.info("No major weaknesses identified.")