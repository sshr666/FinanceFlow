from datetime import datetime


def validate_amount(amount_str):
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return False, "Amount must be a number."
    if amount <= 0:
        return False, "Amount must be greater than zero."
    if amount > 999999999.99:
        return False, "Amount is too large."
    return True, round(amount, 2)


def validate_date(date_str):
    if not date_str:
        return False, "Date is required."
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, date_str
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."


def validate_transaction_type(type_str):
    if type_str not in ("income", "expense"):
        return False, "Type must be 'income' or 'expense'."
    return True, type_str


def validate_category(category_str):
    if not category_str or not category_str.strip():
        return False, "Category is required."
    if len(category_str) > 100:
        return False, "Category name is too long (max 100 characters)."
    return True, category_str.strip()


def validate_description(desc):
    if desc and len(desc) > 500:
        return False, "Description is too long (max 500 characters)."
    return True, desc


def validate_csv_row(row):
    errors = []
    if "type" not in row or not row["type"]:
        errors.append("Missing or empty 'type' column.")
    elif row["type"].strip().lower() not in ("income", "expense"):
        errors.append(f"Invalid type '{row['type']}'. Must be 'income' or 'expense'.")

    if "amount" not in row or not row["amount"]:
        errors.append("Missing or empty 'amount' column.")
    else:
        valid, _ = validate_amount(row["amount"])
        if not valid:
            errors.append(f"Invalid amount '{row['amount']}'.")

    if "category" not in row or not row["category"]:
        errors.append("Missing or empty 'category' column.")

    if "date" not in row or not row["date"]:
        errors.append("Missing or empty 'date' column.")
    else:
        valid, _ = validate_date(row["date"])
        if not valid:
            errors.append(f"Invalid date '{row['date']}'. Use YYYY-MM-DD.")

    return errors
