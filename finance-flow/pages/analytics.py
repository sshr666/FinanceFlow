import streamlit as st
import pandas as pd

from database.crud import get_all_transactions, get_budgets
from analytics.charts import pie_chart, bar_chart, line_chart
from analytics.metrics import (
    category_spending,
    monthly_totals,
    income_vs_expense,
    budget_vs_actual,
)
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state
from config.translations import t


def render():
    st.title(t("page_title_analytics"))

    txns = get_all_transactions()

    if not txns:
        show_empty_state(
            t("empty_analytics_title"),
            t("empty_analytics_message"),
            t("empty_analytics_cta"),
            t("nav_transactions"),
        )
        return

    df = pd.DataFrame(txns)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])

    month, year = get_current_month_year()
    available_months = sorted(df["date"].dt.strftime("%Y-%m").unique())

    selected_month = st.selectbox(
        t("select_month"),
        options=available_months,
        index=len(available_months) - 1 if available_months else 0,
    )
    sel_year, sel_month = int(selected_month.split("-")[0]), int(selected_month.split("-")[1])

    col1, col2 = st.columns(2)

    with col1:
        cat_data = category_spending()
        if cat_data:
            cat_df = pd.DataFrame(
                [{"Category": k, "Amount": v} for k, v in sorted(cat_data.items(), key=lambda x: x[1], reverse=True)]
            )
            st.subheader(t("subheader_category_spending"))
            fig = pie_chart(cat_df, names="Category", values="Amount", title=t("chart_title_spending_by_category"))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        income_dict, expense_dict, months = income_vs_expense()
        if months:
            comp_df = pd.DataFrame(
                {
                    "Month": months,
                    "Income": [income_dict[m] for m in months],
                    "Expenses": [expense_dict[m] for m in months],
                }
            )
            st.subheader(t("subheader_income_vs_expenses"))
            fig = bar_chart(
                comp_df,
                x="Month",
                y=["Income", "Expenses"],
                title=t("chart_title_monthly_income_vs_expenses"),
                barmode="group",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader(t("subheader_monthly_trends"))
    expense_monthly = monthly_totals(type_="expense")
    income_monthly = monthly_totals(type_="income")
    if expense_monthly:
        trend_df = pd.DataFrame(
            {
                "Month": list(expense_monthly.keys()),
                "Spending": list(expense_monthly.values()),
            }
        ).sort_values("Month")
        fig = line_chart(trend_df, x="Month", y="Spending", title=t("chart_title_monthly_spending_trend"))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(t("subheader_budget_utilization"))
    budget_results = budget_vs_actual(sel_month, sel_year)
    if budget_results:
        bud_df = pd.DataFrame(budget_results)
        fig = bar_chart(
            bud_df,
            x="category",
            y=["actual", "limit"],
            title=t("chart_title_budget_vs_actual", month=selected_month),
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(t("info_no_budgets_analytics"))

render()