import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_capital_allocation_data

st.title("💰 Capital Allocation Map")

df = get_capital_allocation_data()
pattern_df = (
    df.groupby("capital_allocation_pattern")
      .size()
      .reset_index(name="Companies")
)
fig = px.treemap(
    pattern_df,
    path=["capital_allocation_pattern"],
    values="Companies",
    color="capital_allocation_pattern",
    title="Capital Allocation Patterns"
)

fig.update_traces(
    textinfo="label+value"
)

fig.update_layout(height=650)

st.plotly_chart(fig, use_container_width=True)
st.divider()

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    sorted(df["capital_allocation_pattern"].unique())
)

companies = df[
    df["capital_allocation_pattern"] == selected_pattern
][[
    "company_name",
    "year",
    "cfo_sign",
    "cfi_sign",
    "cff_sign"
]]

st.subheader(f"Companies in {selected_pattern}")

st.dataframe(
    companies,
    use_container_width=True
)

