import pandas as pd
from database.crud import get_all_transactions, get_budgets


def category_spending(txns=None, type_="expense"):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return {}
    df["amount"] = pd.to_numeric(df["amount"])
    filtered = df[df["type"] == type_]
    return filtered.groupby("category")["amount"].sum().to_dict()


def monthly_totals(txns=None, type_=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return {}
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    if type_:
        df = df[df["type"] == type_]
    return df.groupby("month")["amount"].sum().to_dict()


def income_vs_expense(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return {}, {}, {}
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")

    income = df[df["type"] == "income"].groupby("month")["amount"].sum()
    expense = df[df["type"] == "expense"].groupby("month")["amount"].sum()

    all_months = sorted(set(list(income.index) + list(expense.index)))
    income_dict = {m: income.get(m, 0) for m in all_months}
    expense_dict = {m: expense.get(m, 0) for m in all_months}
    return income_dict, expense_dict, all_months


def budget_vs_actual(month, year, txns=None):
    if txns is None:
        txns = get_all_transactions()
    budgets = get_budgets(month=month, year=year)
    if not budgets:
        return []

    df = pd.DataFrame(txns)
    if df.empty:
        return [
            {
                "category": b["category"],
                "limit": b["limit_amount"],
                "actual": 0,
                "percentage": 0,
            }
            for b in budgets
        ]

    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    month_str = f"{year}-{month:02d}"
    df_month = df[df["date"].dt.strftime("%Y-%m") == month_str]
    expenses = (
        df_month[df_month["type"] == "expense"].groupby("category")["amount"].sum()
    )

    results = []
    for b in budgets:
        actual = expenses.get(b["category"], 0)
        pct = (actual / b["limit_amount"] * 100) if b["limit_amount"] > 0 else 0
        results.append(
            {
                "category": b["category"],
                "limit": b["limit_amount"],
                "actual": round(actual, 2),
                "percentage": round(min(pct, 100), 1),
            }
        )
    return results
