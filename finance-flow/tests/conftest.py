import pytest
import os
import tempfile

from database.connection import init_db


@pytest.fixture(scope="function")
def db_session(monkeypatch):
    from database.crud import _clear_cache

    _clear_cache()
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    monkeypatch.setenv("FINANCEFLOW_DB_PATH", db_path)
    import database.connection as conn_mod

    conn_mod._engine = None
    conn_mod.SessionFactory = None
    init_db()
    yield
    os.unlink(db_path)
    conn_mod._engine = None
    conn_mod.SessionFactory = None
    _clear_cache()


@pytest.fixture(scope="function")
def sample_transactions():
    return [
        {
            "type": "income",
            "amount": 5000.00,
            "category": "Salary",
            "date": "2026-01-15",
            "description": "January salary",
        },
        {
            "type": "income",
            "amount": 5000.00,
            "category": "Salary",
            "date": "2026-02-15",
            "description": "February salary",
        },
        {
            "type": "expense",
            "amount": 200.00,
            "category": "Food",
            "date": "2026-01-16",
            "description": "Groceries",
        },
        {
            "type": "expense",
            "amount": 150.00,
            "category": "Transport",
            "date": "2026-01-17",
            "description": "Gas",
        },
        {
            "type": "expense",
            "amount": 100.00,
            "category": "Food",
            "date": "2026-02-16",
            "description": "Restaurant",
        },
        {
            "type": "expense",
            "amount": 300.00,
            "category": "Utilities",
            "date": "2026-01-20",
            "description": "Electric bill",
        },
    ]


@pytest.fixture(scope="function")
def large_transaction_set():
    import random
    from datetime import datetime, timedelta

    txns = []
    categories = [
        "Food",
        "Transport",
        "Utilities",
        "Entertainment",
        "Shopping",
        "Healthcare",
        "Housing",
    ]
    start_date = datetime(2025, 1, 1)
    for i in range(550):
        date = (start_date + timedelta(days=i % 365)).strftime("%Y-%m-%d")
        txns.append(
            {
                "type": random.choice(["income", "expense"]),
                "amount": round(random.uniform(10, 2000), 2),
                "category": random.choice(categories),
                "date": date,
                "description": f"Transaction {i + 1}",
            }
        )
    return txns
