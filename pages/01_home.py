import streamlit as st
import plotly.express as px
from src.dashboard.utils.db import (
    get_companies,
    get_home_metrics,
    get_sector_count,
    get_avg_roe,
    get_median_pe,
    get_company_count,
    get_sector_distribution,
    get_median_de,
    get_median_revenue_cagr,
get_top_quality_companies,
get_debt_free_count,
)



st.title("🏠 Home")

# Sidebar
selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

companies = get_companies()
ratios = get_home_metrics(selected_year)
sector_count = get_sector_count()
avg_roe = get_avg_roe(selected_year)
median_pe = get_median_pe(selected_year)
company_count = get_company_count()
sector_data = get_sector_distribution()
median_de = get_median_de(selected_year)
median_revenue_cagr = get_median_revenue_cagr()
debt_free_count = get_debt_free_count(selected_year)
top_quality = get_top_quality_companies(selected_year)



st.write(f"### Financial Year: {selected_year}")



col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
with col1:
    st.metric(
        "📈 Total Companies",
        company_count
    )

with col2:
    st.metric(
        "🏦 Debt-Free Companies",
        debt_free_count
    )

with col3:
    st.metric(
        "💹 Average ROE",
        f"{avg_roe}%"
    )

with col4:
    st.metric(
        "📊 Median P/E",
        median_pe
    )
with col5:
    st.metric(
        "📉 Median D/E",
        median_de
    )

with col6:
    st.metric(
        "📈 Revenue CAGR (5yr)",
        f"{median_revenue_cagr}%"
    )
st.subheader("🏭 Sector Distribution")

fig = px.pie(
    sector_data,
    names="broad_sector",
    values="company_count",
    hole=0.5
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    height=420,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🏆 Top 5 Companies by Composite Quality Score")

st.dataframe(
    top_quality,
    width="stretch",
    hide_index=True
)