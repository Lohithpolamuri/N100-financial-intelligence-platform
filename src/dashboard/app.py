from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PAGES = PROJECT_ROOT / "pages"

home = st.Page(PAGES / "01_home.py", title="Home", icon="🏠", default=True)
profile = st.Page(PAGES / "02_profile.py", title="Company Profile", icon="🏢")
screener = st.Page(PAGES / "03_screener.py", title="Screener", icon="📊")
peers = st.Page(PAGES / "04_peers.py", title="Peer Comparison", icon="🤝")
trends = st.Page(PAGES / "05_trends.py", title="Trend Analysis", icon="📈")
sectors = st.Page(PAGES / "06_sectors.py", title="Sector Analysis", icon="🏭")
capital = st.Page(PAGES / "07_capital.py", title="Capital Allocation", icon="💰")
reports = st.Page(PAGES / "08_reports.py", title="Annual Reports", icon="📄")

pg = st.navigation(
    [
        home,
        profile,
        screener,
        peers,
        trends,
        sectors,
        capital,
        reports,
    ]
)

pg.run()