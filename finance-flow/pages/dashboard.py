import streamlit as st
import pandas as pd
from datetime import datetime

from database.crud import get_all_transactions
from analytics.charts import line_chart
from utils.helpers import get_current_month_year
from utils.empty_states import show_empty_state


def render():
    st.title("📊 Dashboard")

    txns = get_all_transactions()

    if not txns:
        show_empty_state(
            "Welcome to FinanceFlow!",
            "Start tracking your finances by adding your first transaction. "
            "Visit the Transactions page to get started.",
            "Go to Transactions",
            "/Transactions",
        )
        return

    df = pd.DataFrame(txns)
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])

    month, year = get_current_month_year()
    month_str = f"{year}-{month:02d}"

    df_month = df[df["date"].dt.strftime("%Y-%m") == month_str]

    income = df_month[df_month["type"] == "income"]["amount"].sum()
    expenses = df_month[df_month["type"] == "expense"]["amount"].sum()
    balance = df[df["type"] == "income"]["amount"].sum() - df[df["type"] == "expense"]["amount"].sum()

    savings = income - expenses

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Balance", f"${balance:,.2f}")
    with col2:
        st.metric("Monthly Income", f"${income:,.2f}")
    with col3:
        st.metric("Monthly Spending", f"${expenses:,.2f}")
    with col4:
        delta = savings
        st.metric("Monthly Savings", f"${savings:,.2f}", delta=f"${delta:,.2f}")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Recent Transactions")
        recent = sorted(txns, key=lambda t: t["date"], reverse=True)[:10]
        for t in recent:
            sign = "+" if t["type"] == "income" else "-"
            color = "green" if t["type"] == "income" else "red"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:4px 0;'>"
                f"<span>{t['date']} - {t['category']}</span>"
                f"<span style='color:{color};font-weight:bold;'>{sign}${t['amount']:,.2f}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    with col_b:
        st.subheader("Monthly Spending Trend")
        df["month"] = df["date"].dt.strftime("%Y-%m")
        daily_expense = (
            df[df["type"] == "expense"]
            .groupby("date")["amount"]
            .sum()
            .reset_index()
            .sort_values("date")
        )
        if not daily_expense.empty:
            fig = line_chart(
                daily_expense.tail(30),
                x="date",
                y="amount",
                title="Daily Expenses (Last 30 days)",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expense data to show trend.")

render()