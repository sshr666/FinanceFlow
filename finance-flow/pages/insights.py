import streamlit as st
import pandas as pd
from datetime import datetime

from database.crud import get_all_transactions, get_budgets, set_setting
from analytics.insights import (
    highest_spending_category,
    average_monthly_spend,
    month_over_month_change,
    savings_rate,
    spending_trend_direction,
    get_savings_target,
)
from analytics.metrics import budget_vs_actual
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state


def render():
    st.title("💡 Insights")

    txns = get_all_transactions()

    if not txns:
        show_empty_state(
            "Not enough data",
            "Track transactions for at least one month to see spending insights.",
            "Go to Transactions",
            "/Transactions",
        )
        return

    month, year = get_current_month_year()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💳 Spending Patterns")
        top_cat = highest_spending_category()
        if top_cat:
            st.metric("Highest Spending Category", top_cat)

        avg_spend = average_monthly_spend()
        st.metric("Average Monthly Spend", f"${avg_spend:,.2f}")

        change = month_over_month_change()
        if change is not None:
            delta = f"{change}%"
            st.metric("Month-over-Month Change", f"{change:+.1f}%", delta=delta)
        else:
            st.metric("Month-over-Month Change", "N/A (need 2+ months)")

    with col2:
        st.subheader("💰 Savings & Trends")
        s_rate = savings_rate()
        st.metric("Savings Rate", f"{s_rate}%")

        direction = spending_trend_direction()
        emoji = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}
        st.metric("Spending Trend", f"{emoji.get(direction, '➡️')} {direction.capitalize()}")

        target = get_savings_target()
        st.metric("Savings Target", f"${target:,.2f}/month" if target > 0 else "Not set")

    st.divider()

    st.subheader("🎯 Savings Goal")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        new_target = st.number_input("Set monthly savings target ($)", min_value=0.0, format="%.2f", value=target)
    with col_b:
        if st.button("Save Target", type="primary"):
            set_setting("savings_target", str(new_target))
            st.success(f"Savings target set to ${new_target:,.2f}")
            st.rerun()

    if target > 0 and txns:
        df = pd.DataFrame(txns)
        df["amount"] = pd.to_numeric(df["amount"])
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expenses = df[df["type"] == "expense"]["amount"].sum()
        saved = total_income - total_expenses
        progress = min(saved / target, 1.0) if target > 0 else 0
        st.progress(progress)
        st.markdown(f"**Saved:** ${saved:,.2f} / **Target:** ${target:,.2f}")

    st.divider()

    st.subheader("🚨 Budget Alerts")
    budget_results = budget_vs_actual(month, year)
    if budget_results:
        for r in budget_results:
            if r["percentage"] >= 80:
                emoji = "🔴" if r["percentage"] >= 100 else "🟠"
                st.warning(
                    f"{emoji} **{r['category']}**: {r['percentage']}% used "
                    f"(${r['actual']:,.2f} / ${r['limit']:,.2f})"
                )
        if not any(r["percentage"] >= 80 for r in budget_results):
            st.success("✅ All budgets are within limits!")
    else:
        st.info("No budgets set. Go to Budgets page to create spending limits.")
