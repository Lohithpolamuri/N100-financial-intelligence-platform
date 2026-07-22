import streamlit as st

from src.dashboard.utils.db import get_screener_data

st.title("📊 Stock Screener")

df = get_screener_data()
defaults = {
    "roe": float(df["return_on_equity_pct"].min()),
    "de": float(df["debt_to_equity"].max()),
    "fcf": float(df["free_cash_flow_cr"].min()),
    "rev": float(df["revenue_cagr_5yr"].min()),
    "pat": float(df["pat_cagr_5yr"].min()),
    "opm": float(df["operating_profit_margin_pct"].min()),
    "pe": float(df["pe_ratio"].max()),
    "pb": float(df["pb_ratio"].max()),
    "div": float(df["dividend_yield_pct"].min()),
    "icr": float(df["interest_coverage"].min()),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.sidebar.header("Filters")
st.sidebar.subheader("Quick Presets")

c1, c2 = st.sidebar.columns(2)
c3, c4 = st.sidebar.columns(2)
c5, c6 = st.sidebar.columns(2)

if c1.button("⭐ Quality"):
    st.session_state.roe = 8
    st.session_state.de = 2
    st.session_state.opm = 8
    st.rerun()

if c2.button("💰 Value"):
    st.session_state.pe = 35
    st.session_state.pb = 6
    st.rerun()

if c3.button("📈 Growth"):
    st.session_state.rev = 5
    st.session_state.pat = 5
    st.rerun()

if c4.button("💸 Dividend"):
    st.session_state.div = 0.5
    st.rerun()

if c5.button("🏦 Debt-Free"):
    st.session_state.de = 2
    st.rerun()

if c6.button("🔄 Turnaround"):
    st.session_state.fcf = -500
    st.session_state.roe = 0
    st.rerun()
roe_min = st.sidebar.slider(
    "ROE (%)",
    float(df["return_on_equity_pct"].min()),
    float(df["return_on_equity_pct"].max()),
    key="roe"
)

de_max = st.sidebar.slider(
    "Debt / Equity",
    float(df["debt_to_equity"].min()),
    float(df["debt_to_equity"].max()),
    key="de"
)

fcf_min = st.sidebar.slider(
    "Free Cash Flow",
    float(df["free_cash_flow_cr"].min()),
    float(df["free_cash_flow_cr"].max()),
    key ="fcf"
)

revenue_cagr_min = st.sidebar.slider(
    "Revenue CAGR (5Y)",
    float(df["revenue_cagr_5yr"].min()),
    float(df["revenue_cagr_5yr"].max()),
    key="rev"
)

pat_cagr_min = st.sidebar.slider(
    "PAT CAGR (5Y)",
    float(df["pat_cagr_5yr"].min()),
    float(df["pat_cagr_5yr"].max()),
    key="pat"
)

opm_min = st.sidebar.slider(
    "Operating Profit Margin",
    float(df["operating_profit_margin_pct"].min()),
    float(df["operating_profit_margin_pct"].max()),
    key="opm"
)

pe_max = st.sidebar.slider(
    "P/E Ratio",
    float(df["pe_ratio"].min()),
    float(df["pe_ratio"].max()),
    key="pe"
)

pb_max = st.sidebar.slider(
    "P/B Ratio",
    float(df["pb_ratio"].min()),
    float(df["pb_ratio"].max()),
    key="pb"
)

dividend_min = st.sidebar.slider(
    "Dividend Yield",
    float(df["dividend_yield_pct"].min()),
    float(df["dividend_yield_pct"].max()),
    key="div"
)

icr_min = st.sidebar.slider(
    "Interest Coverage Ratio",
    float(df["interest_coverage"].min()),
    float(df["interest_coverage"].max()),
    key="icr"
)

filtered = df[
    (df["return_on_equity_pct"] >= roe_min) &
    (df["debt_to_equity"] <= de_max) &
    (df["free_cash_flow_cr"] >= fcf_min) &
    (df["revenue_cagr_5yr"] >= revenue_cagr_min) &
    (df["pat_cagr_5yr"] >= pat_cagr_min) &
    (df["operating_profit_margin_pct"] >= opm_min) &
    (df["pe_ratio"] <= pe_max) &
    (df["pb_ratio"] <= pb_max) &
    (df["dividend_yield_pct"] >= dividend_min) &
    (df["interest_coverage"] >= icr_min)
]

st.subheader(f"📈 {len(filtered)} companies match your filters")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download CSV",
    filtered.to_csv(index=False),
    "screener_results.csv",
    "text/csv"
)