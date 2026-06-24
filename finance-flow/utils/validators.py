from datetime import datetime
from config.translations import t


def validate_amount(amount_str):
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return False, t("error_amount_number")
    if amount <= 0:
        return False, t("error_amount_positive")
    if amount > 999999999.99:
        return False, t("error_amount_too_large")
    return True, round(amount, 2)


def validate_date(date_str):
    if not date_str:
        return False, t("error_date_required")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, date_str
    except ValueError:
        return False, t("error_date_format")


def validate_category(category_str):
    if not category_str or not category_str.strip():
        return False, t("error_category_required")
    if len(category_str) > 100:
        return False, t("error_category_too_long")
    return True, category_str.strip()


def validate_description(desc):
    if desc and len(desc) > 500:
        return False, t("error_description_too_long")
    return True, desc


def validate_csv_row(row):
    errors = []
    if "type" not in row or not row["type"]:
        errors.append(t("error_csv_missing_type"))
    elif row["type"].strip().lower() not in ("income", "expense"):
        errors.append(t("error_csv_invalid_type", type=row["type"]))

    if "amount" not in row or not row["amount"]:
        errors.append(t("error_csv_missing_amount"))
    else:
        valid, _ = validate_amount(row["amount"])
        if not valid:
            errors.append(t("error_csv_invalid_amount", amount=row["amount"]))

    if "category" not in row or not row["category"]:
        errors.append(t("error_csv_missing_category"))

    if "date" not in row or not row["date"]:
        errors.append(t("error_csv_missing_date"))
    else:
        valid, _ = validate_date(row["date"])
        if not valid:
            errors.append(t("error_csv_invalid_date", date=row["date"]))

    return errors
