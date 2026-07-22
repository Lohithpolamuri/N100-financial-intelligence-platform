import streamlit as st
import requests
import pandas as pd

from src.dashboard.utils.db import get_annual_reports
@st.cache_data(ttl=3600)
def url_exists(url):
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=5
        )
        return response.status_code != 404
    except Exception:
        return False

st.title("📄 Annual Reports")

df = get_annual_reports()


company = st.selectbox(
    "Select Company",
    sorted(df["company_name"].dropna().unique())
)


company_df = (
    df[df["company_name"] == company]
      .sort_values("Year", ascending=False)
)

st.subheader(company)

for _, row in company_df.iterrows():

    year = row["Year"]
    url = row["Annual_Report"]

    if pd.notna(url) and str(url).startswith("http"):

        if url_exists(url):

            st.link_button(
                f"📄 {year} Annual Report",
                url,
                use_container_width=True
            )

        else:

            st.error(f"🔴 {year} - Report Unavailable")

    else:

        st.error(f"🔴 {year} - Report Unavailable")