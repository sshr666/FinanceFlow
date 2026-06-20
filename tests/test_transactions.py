from database.crud import (
    add_transaction,
    update_transaction,
    delete_transaction,
    get_all_transactions,
)


class TestTransactionCalculations:
    def test_balance_calculation(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        txns = get_all_transactions()
        total_income = sum(t["amount"] for t in txns if t["type"] == "income")
        total_expense = sum(t["amount"] for t in txns if t["type"] == "expense")
        assert total_income == 10000.00
        assert total_expense == 750.00
        assert total_income - total_expense == 9250.00

    def test_edit_recalculation(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        txns = get_all_transactions()
        expense_txn = [t for t in txns if t["type"] == "expense"][0]
        original_amount = expense_txn["amount"]
        update_transaction(expense_txn["id"], amount=500.00)
        updated_txns = get_all_transactions()
        total_expense_before = sum(t["amount"] for t in txns if t["type"] == "expense")
        total_expense_after = sum(
            t["amount"] for t in updated_txns if t["type"] == "expense"
        )
        assert total_expense_after == total_expense_before - original_amount + 500.00

    def test_delete_recalculation(self, db_session):
        add_transaction("income", 1000.00, "Salary", "2026-01-01")
        txn2 = add_transaction("expense", 300.00, "Food", "2026-01-02")
        add_transaction("expense", 200.00, "Transport", "2026-01-03")
        delete_transaction(txn2)
        txns = get_all_transactions()
        total_expense = sum(t["amount"] for t in txns if t["type"] == "expense")
        total_income = sum(t["amount"] for t in txns if t["type"] == "income")
        assert total_income == 1000.00
        assert total_expense == 200.00
