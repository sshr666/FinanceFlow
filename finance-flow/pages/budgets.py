import streamlit as st
from datetime import datetime

from database.crud import get_budgets, set_budget, delete_budget, get_all_transactions
from analytics.metrics import budget_vs_actual
from config.settings import get_config_int
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state
from config.translations import t


def render():
    st.title(t("page_title_budgets"))

    month, year = get_current_month_year()
    txns = get_all_transactions()

    tab1, tab2 = st.tabs([t("tab_budget_overview"), t("tab_manage_budgets")])

    with tab1:
        _render_budget_overview(month, year)

    with tab2:
        _render_budget_management(month, year)

    budgets = get_budgets(month=month, year=year)
    if not budgets:
        show_empty_state(
            t("empty_budgets_title"),
            t("empty_budgets_message"),
            t("empty_budgets_cta"),
            t("nav_budgets"),
        )


def _render_budget_overview(month, year):
    st.subheader(t("subheader_budget_overview", date=datetime(year, month, 1).strftime('%B %Y')))

    results = budget_vs_actual(month, year)
    threshold = get_config_int("BUDGET_ALERT_THRESHOLD", 80)

    if not results:
        st.info(t("info_no_budgets_month"))
        return

    for r in results:
        pct = r["percentage"]
        st.markdown('<div class="budget-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.markdown(f'<span class="budget-category">{r["category"]}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<span class="budget-spend">${r["actual"]:,.2f} / ${r["limit"]:,.2f}</span>', unsafe_allow_html=True)
        with col3:
            if pct >= 100:
                st.markdown(f'<span class="budget-alert-danger">{pct}%</span>', unsafe_allow_html=True)
            elif pct >= threshold:
                st.markdown(f'<span class="budget-alert-warning">{pct}%</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color:#94a3b8;font-weight:600;font-size:0.9rem;">{pct}%</span>', unsafe_allow_html=True)
        with col4:
            remaining = r["limit"] - r["actual"]
            st.progress(min(pct / 100, 1.0))
            if remaining < 0:
                st.markdown(f'<span class="budget-alert-danger">${abs(remaining):,.2f} {t("label_over_suffix")}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color:#94a3b8;font-size:0.85rem;">${remaining:,.2f} {t("label_remaining_suffix")}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if pct >= 100:
            st.warning(t("warning_budget_exceeded", category=r['category'], limit=r['limit'], actual=r['actual']))
        elif pct >= threshold:
            st.warning(t("warning_budget_nearing", category=r['category'], pct=pct))


def _render_budget_management(month, year):
    st.subheader(t("subheader_add_edit_budget"))

    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.text_input(t("form_category_name"), placeholder=t("placeholder_category_name"))
            limit_amount = st.number_input(t("form_monthly_limit"), min_value=0.01, format="%.2f")
        with col2:
            sel_month = st.selectbox(t("form_month"), range(1, 13), index=month - 1)
            sel_year = st.number_input(t("form_year"), min_value=2020, max_value=2100, value=year)

        if st.form_submit_button(t("btn_save_budget"), type="primary", use_container_width=True):
            if category and limit_amount > 0:
                set_budget(category.strip(), sel_month, sel_year, limit_amount)
                st.success(t("success_budget_saved", category=category, limit=limit_amount))
                st.rerun()
            else:
                st.error(t("error_budget_required"))

    st.subheader(t("subheader_existing_budgets"))
    budgets = get_budgets(month=month, year=year)
    if budgets:
        for b in budgets:
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"**{b['category']}**")
            with c2:
                st.write(f"${b['limit_amount']:,.2f}{t('per_month')}")
            with c3:
                if st.button("🗑️", key=f"del_budget_{b['id']}"):
                    delete_budget(b["id"])
                    st.rerun()

render()