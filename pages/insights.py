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
from analytics.ai_insights import get_ai_insights
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state
from config.translations import t


def render():
    st.title(t("page_title_insights"))

    txns = get_all_transactions()

    if not txns:
        show_empty_state(
            t("empty_insights_title"),
            t("empty_insights_message"),
            t("empty_insights_cta"),
            t("nav_transactions"),
        )
        return

    month, year = get_current_month_year()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("subheader_spending_patterns"))
        top_cat = highest_spending_category()
        if top_cat:
            st.metric(t("metric_highest_spending_category"), top_cat)

        avg_spend = average_monthly_spend()
        st.metric(t("metric_average_monthly_spend"), f"${avg_spend:,.2f}")

        change = month_over_month_change()
        if change is not None:
            delta = f"{change}%"
            st.metric(t("metric_month_over_month_change"), f"{change:+.1f}%", delta=delta)
        else:
            st.metric(t("metric_month_over_month_change"), t("na_need_more_months"))

    with col2:
        st.subheader(t("subheader_savings_trends"))
        s_rate = savings_rate()
        st.metric(t("metric_savings_rate"), f"{s_rate}%")

        direction = spending_trend_direction()
        trend_labels = {"increasing": t("trend_increasing"), "decreasing": t("trend_decreasing"), "stable": t("trend_stable")}
        emoji = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}
        st.metric(t("metric_spending_trend"), f"{emoji.get(direction, '➡️')} {trend_labels.get(direction, direction).capitalize()}")

        target = get_savings_target()
        st.metric(t("metric_savings_target"), f"${target:,.2f}/month" if target > 0 else t("label_not_set"))

    st.divider()

    st.subheader(t("subheader_savings_goal"))
    col_a, col_b = st.columns([2, 1])
    with col_a:
        new_target = st.number_input(t("form_savings_target"), min_value=0.0, format="%.2f", value=target)
    with col_b:
        if st.button(t("btn_save_target"), type="primary"):
            set_setting("savings_target", str(new_target))
            st.success(t("success_target_set", target=new_target))
            st.rerun()

    if target > 0 and txns:
        df = pd.DataFrame(txns)
        df["amount"] = pd.to_numeric(df["amount"])
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expenses = df[df["type"] == "expense"]["amount"].sum()
        saved = total_income - total_expenses
        progress = min(saved / target, 1.0) if target > 0 else 0
        st.progress(progress)
        st.markdown(t("label_saved_vs_target", saved=saved, target=target))

    st.divider()

    st.subheader(t("subheader_budget_alerts"))
    budget_results = budget_vs_actual(month, year)
    if budget_results:
        for r in budget_results:
            if r["percentage"] >= 80:
                st.warning(
                    f"{'🔴' if r['percentage'] >= 100 else '🟠'} **{r['category']}**: {r['percentage']}% used "
                    f"(${r['actual']:,.2f} / ${r['limit']:,.2f})"
                )
        if not any(r["percentage"] >= 80 for r in budget_results):
            st.success(t("success_all_budgets_within_limits"))
    else:
        st.info(t("info_no_budgets_insights"))

    st.divider()

    st.subheader("🤖 AI Insights")
    st.caption("Get AI-powered financial recommendations based on your transaction data. Uses local Ollama.")

    if st.button("✨ Generate AI Insights", type="secondary", use_container_width=True):
        lang = st.session_state.get("lang", "en")
        with st.spinner("Analyzing your transactions with AI..."):
            insights, error = get_ai_insights(txns, lang=lang)
        if error:
            st.warning(f"⚠️ {error}")
        else:
            st.success("✅ AI analysis complete!")
            st.markdown(insights)

render()
