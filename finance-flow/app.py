import streamlit as st

from config.settings import get_config
from config.styling import apply_theme
from database.connection import init_db
from config.categories import ensure_default_categories

st.set_page_config(
    page_title="FinanceFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()
ensure_default_categories()

pages = {
    "Dashboard": st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    "Transactions": st.Page("pages/transactions.py", title="Transactions", icon="💳"),
    "Analytics": st.Page("pages/analytics.py", title="Analytics", icon="📈"),
    "Budgets": st.Page("pages/budgets.py", title="Budgets", icon="🎯"),
    "CSV Tools": st.Page("pages/csv_tools.py", title="CSV Tools", icon="📁"),
    "Insights": st.Page("pages/insights.py", title="Insights", icon="💡"),
}

nav = st.navigation(list(pages.values()))
nav.run()
