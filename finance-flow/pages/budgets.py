import streamlit as st
from datetime import datetime

from database.crud import get_budgets, set_budget, delete_budget, get_all_transactions
from analytics.metrics import budget_vs_actual
from config.settings import get_config_int
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state


def render():
    st.title("🎯 Budgets")

    month, year = get_current_month_year()
    txns = get_all_transactions()

    tab1, tab2 = st.tabs(["Budget Overview", "Manage Budgets"])

    with tab1:
        _render_budget_overview(month, year)

    with tab2:
        _render_budget_management(month, year)

    budgets = get_budgets(month=month, year=year)
    if not budgets:
        show_empty_state(
            "No budgets set",
            "Create monthly budgets to track your spending limits.",
            "Set a Budget",
            "/Budgets",
        )


def _render_budget_overview(month, year):
    st.subheader(f"Budget Overview - {datetime(year, month, 1).strftime('%B %Y')}")

    results = budget_vs_actual(month, year)
    threshold = get_config_int("BUDGET_ALERT_THRESHOLD", 80)

    if not results:
        st.info("No budgets configured for this month.")
        return

    for r in results:
        pct = r["percentage"]
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.markdown(f"**{r['category']}**")
        with col2:
            st.markdown(f"${r['actual']:,.2f} / ${r['limit']:,.2f}")
        with col3:
            if pct >= 100:
                st.markdown(f'<span class="budget-alert-danger">{pct}%</span>', unsafe_allow_html=True)
            elif pct >= threshold:
                st.markdown(f'<span class="budget-alert-warning">{pct}%</span>', unsafe_allow_html=True)
            else:
                st.markdown(f"{pct}%")
        with col4:
            remaining = r["limit"] - r["actual"]
            st.progress(min(pct / 100, 1.0))
            if remaining < 0:
                st.markdown(f'<span class="budget-alert-danger">${abs(remaining):,.2f} over</span>', unsafe_allow_html=True)
            else:
                st.markdown(f"${remaining:,.2f} remaining")
        if pct >= 100:
            st.warning(f"⚠️ {r['category']} budget exceeded! Limit: ${r['limit']:,.2f}, Spent: ${r['actual']:,.2f}")
        elif pct >= threshold:
            st.warning(f"⚡ {r['category']} nearing limit ({pct}% used)")
        st.divider()


def _render_budget_management(month, year):
    st.subheader("Add / Edit Budget")

    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.text_input("Category name", placeholder="e.g., Food")
            limit_amount = st.number_input("Monthly limit ($)", min_value=0.01, format="%.2f")
        with col2:
            sel_month = st.selectbox("Month", range(1, 13), index=month - 1)
            sel_year = st.number_input("Year", min_value=2020, max_value=2100, value=year)

        if st.form_submit_button("💾 Save Budget", type="primary", use_container_width=True):
            if category and limit_amount > 0:
                set_budget(category.strip(), sel_month, sel_year, limit_amount)
                st.success(f"Budget saved for '{category}' - ${limit_amount:,.2f}/month")
                st.rerun()
            else:
                st.error("Category name and positive limit are required.")

    st.subheader("Existing Budgets")
    budgets = get_budgets(month=month, year=year)
    if budgets:
        for b in budgets:
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"**{b['category']}**")
            with c2:
                st.write(f"${b['limit_amount']:,.2f}/month")
            with c3:
                if st.button("🗑️", key=f"del_budget_{b['id']}"):
                    delete_budget(b["id"])
                    st.rerun()

render()