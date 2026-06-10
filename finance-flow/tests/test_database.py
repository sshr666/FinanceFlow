import pytest
from datetime import datetime

from database.connection import init_db, get_engine, get_session
from database.models import Base, Transaction, Budget, Settings
from database.crud import (
    add_transaction,
    get_all_transactions,
    update_transaction,
    delete_transaction,
    get_transaction_by_id,
    set_budget,
    get_budgets,
    delete_budget,
    set_setting,
    get_setting,
)


class TestTransactionCRUD:
    def test_add_transaction(self, db_session):
        txn_id = add_transaction("income", 1000.00, "Salary", "2026-01-01", "Test")
        assert txn_id is not None

    def test_get_all_transactions(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        txns = get_all_transactions()
        assert len(txns) == len(sample_transactions)

    def test_update_transaction(self, db_session):
        txn_id = add_transaction("expense", 50.00, "Food", "2026-01-01")
        result = update_transaction(txn_id, amount=75.00)
        assert result is True
        updated = get_transaction_by_id(txn_id)
        assert updated["amount"] == 75.00

    def test_delete_transaction(self, db_session):
        txn_id = add_transaction("expense", 30.00, "Transport", "2026-01-01")
        result = delete_transaction(txn_id)
        assert result is True
        assert get_transaction_by_id(txn_id) is None

    def test_delete_nonexistent(self, db_session):
        result = delete_transaction(9999)
        assert result is False


class TestBudgetCRUD:
    def test_set_budget(self, db_session):
        set_budget("Food", 1, 2026, 500.00)
        budgets = get_budgets(month=1, year=2026)
        assert len(budgets) == 1
        assert budgets[0]["limit_amount"] == 500.00

    def test_budget_uniqueness(self, db_session):
        set_budget("Food", 1, 2026, 500.00)
        set_budget("Food", 1, 2026, 600.00)
        budgets = get_budgets(month=1, year=2026)
        assert len(budgets) == 1
        assert budgets[0]["limit_amount"] == 600.00

    def test_delete_budget(self, db_session):
        set_budget("Transport", 2, 2026, 200.00)
        budgets = get_budgets(month=2, year=2026)
        assert len(budgets) == 1
        delete_budget(budgets[0]["id"])
        assert len(get_budgets(month=2, year=2026)) == 0


class TestSettingsCRUD:
    def test_set_and_get(self, db_session):
        set_setting("test_key", "test_value")
        assert get_setting("test_key") == "test_value"

    def test_get_default(self, db_session):
        assert get_setting("nonexistent", "default") == "default"

    def test_update_setting(self, db_session):
        set_setting("key", "value1")
        set_setting("key", "value2")
        assert get_setting("key") == "value2"
