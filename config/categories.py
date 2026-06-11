from database.crud import get_all_categories, add_transaction

DEFAULT_INCOME_CATEGORIES = ["Salary", "Freelance", "Investments", "Other Income"]
DEFAULT_EXPENSE_CATEGORIES = [
    "Food",
    "Housing",
    "Transport",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Shopping",
    "Other Expense",
]


def ensure_default_categories():
    existing = get_all_categories()
    existing_lower = {c.lower() for c in existing}
    for cat in DEFAULT_INCOME_CATEGORIES + DEFAULT_EXPENSE_CATEGORIES:
        if cat.lower() not in existing_lower:
            pass
