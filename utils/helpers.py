from datetime import datetime


def format_currency(amount, currency="USD"):
    if currency == "USD":
        if amount >= 0:
            return f"${amount:,.2f}"
        return f"-${abs(amount):,.2f}"
    return f"{amount:,.2f}"


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def get_current_month_year():
    now = datetime.now()
    return now.month, now.year


def filter_transactions(
    txns, start_date=None, end_date=None, category=None, type_=None
):
    result = txns
    if start_date:
        result = [t for t in result if t["date"] >= start_date]
    if end_date:
        result = [t for t in result if t["date"] <= end_date]
    if category:
        result = [t for t in result if t["category"] == category]
    if type_:
        result = [t for t in result if t["type"] == type_]
    return result
