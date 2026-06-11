import streamlit as st

from config.settings import get_config
from config.styling import apply_theme
from database.connection import init_db
from config.categories import ensure_default_categories
from config.translations import t

st.set_page_config(
    page_title="FinanceFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_db()
ensure_default_categories()

if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

pages = {
    t("nav_dashboard"): st.Page("pages/dashboard.py", title=t("nav_dashboard"), icon="📊"),
    t("nav_transactions"): st.Page("pages/transactions.py", title=t("nav_transactions"), icon="💳"),
    t("nav_analytics"): st.Page("pages/analytics.py", title=t("nav_analytics"), icon="📈"),
    t("nav_budgets"): st.Page("pages/budgets.py", title=t("nav_budgets"), icon="🎯"),
    t("nav_csv_tools"): st.Page("pages/csv_tools.py", title=t("nav_csv_tools"), icon="📁"),
    t("nav_insights"): st.Page("pages/insights.py", title=t("nav_insights"), icon="💡"),
}

with st.sidebar:
    st.selectbox(
        t("lang_label"),
        options=["en", "hi", "te"],
        format_func=lambda x: {"en": t("lang_en"), "hi": t("lang_hi"), "te": t("lang_te")}[x],
        key="lang",
    )

nav = st.navigation(list(pages.values()))
nav.run()
