from datetime import datetime


def get_current_month_year():
    now = datetime.now()
    return now.month, now.year
