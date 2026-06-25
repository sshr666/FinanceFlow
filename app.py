import streamlit as st

from config.styling import apply_theme
from database.connection import init_db
from config.categories import ensure_default_categories
from config.translations import t
from database.auth import login, signup

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

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

with st.sidebar:
    st.selectbox(
        t("lang_label"),
        options=["en", "hi", "ta"],
        format_func=lambda x: {
            "en": t("lang_en"),
            "hi": t("lang_hi"),
            "ta": t("lang_ta"),
        }[x],
        key="lang",
    )
    st.divider()

    if st.session_state["user_id"] is not None:
        st.caption(
            t("label_logged_in_as", username=st.session_state.get("username", ""))
        )
        if st.button(t("btn_logout"), type="secondary", use_container_width=True):
            st.session_state["user_id"] = None
            st.session_state["username"] = None
            st.session_state.pop("lang", None)
            st.rerun()

if st.session_state["user_id"] is None:
    st.title(t("page_title_auth"))
    tab1, tab2 = st.tabs([t("tab_login"), t("tab_signup")])

    with tab1:
        with st.form("login_form"):
            username = st.text_input(t("form_username"))
            password = st.text_input(t("form_password"), type="password")
            if st.form_submit_button(
                t("btn_login"), type="primary", use_container_width=True
            ):
                user_id, err = login(username, password)
                if err:
                    st.error(err)
                else:
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                    st.rerun()

    with tab2:
        with st.form("signup_form"):
            username = st.text_input(t("form_choose_username"))
            password = st.text_input(t("form_choose_password"), type="password")
            if st.form_submit_button(
                t("btn_signup"), type="primary", use_container_width=True
            ):
                user_id, err = signup(username, password)
                if err:
                    st.error(err)
                else:
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = username
                    st.rerun()
else:
    pages = {
        t("nav_dashboard"): st.Page(
            "pages/dashboard.py", title=t("nav_dashboard"), icon="📊"
        ),
        t("nav_transactions"): st.Page(
            "pages/transactions.py", title=t("nav_transactions"), icon="💳"
        ),
        t("nav_analytics"): st.Page(
            "pages/analytics.py", title=t("nav_analytics"), icon="📈"
        ),
        t("nav_budgets"): st.Page(
            "pages/budgets.py", title=t("nav_budgets"), icon="🎯"
        ),
        t("nav_csv_tools"): st.Page(
            "pages/csv_tools.py", title=t("nav_csv_tools"), icon="📁"
        ),
        t("nav_insights"): st.Page(
            "pages/insights.py", title=t("nav_insights"), icon="💡"
        ),
        t("nav_reviews"): st.Page(
            "pages/reviews.py", title=t("nav_reviews"), icon="⭐"
        ),
    }

    nav = st.navigation(list(pages.values()))
    nav.run()
