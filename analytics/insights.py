import pandas as pd
from database.crud import get_all_transactions, get_budgets, get_setting


def highest_spending_category(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return None
    df["amount"] = pd.to_numeric(df["amount"])
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return None
    return expenses.groupby("category")["amount"].sum().idxmax()


def average_monthly_spend(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return 0
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return 0
    monthly = expenses.groupby("month")["amount"].sum()
    return round(monthly.mean(), 2)


def month_over_month_change(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return None
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return None
    monthly = expenses.groupby("month")["amount"].sum().sort_index()
    if len(monthly) < 2:
        return None
    last_month = monthly.iloc[-1]
    prev_month = monthly.iloc[-2]
    if prev_month == 0:
        return None
    return round(((last_month - prev_month) / prev_month) * 100, 1)


def savings_rate(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return 0
    df["amount"] = pd.to_numeric(df["amount"])
    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expenses = df[df["type"] == "expense"]["amount"].sum()
    if total_income == 0:
        return 0
    return round(((total_income - total_expenses) / total_income) * 100, 1)


def spending_trend_direction(txns=None):
    if txns is None:
        txns = get_all_transactions()
    df = pd.DataFrame(txns)
    if df.empty:
        return "stable"
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return "stable"
    monthly = expenses.groupby("month")["amount"].sum()
    if len(monthly) < 2:
        return "stable"
    recent = monthly.tail(3)
    if len(recent) < 2:
        return "stable"
    if recent.iloc[-1] > recent.iloc[-2]:
        return "increasing"
    elif recent.iloc[-1] < recent.iloc[-2]:
        return "decreasing"
    return "stable"


def get_savings_target():
    target = get_setting("savings_target")
    if target:
        try:
            return float(target)
        except ValueError:
            return 0
    return 0
