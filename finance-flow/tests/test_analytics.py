from database.crud import add_transaction
from analytics.metrics import (
    category_spending,
    monthly_totals,
    income_vs_expense,
    budget_vs_actual,
)
from analytics.insights import (
    highest_spending_category,
    average_monthly_spend,
    savings_rate,
)


class TestAnalyticsMetrics:
    def test_category_spending(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        spending = category_spending()
        assert "Food" in spending
        assert spending["Food"] == 300.00

    def test_monthly_totals(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        totals = monthly_totals(type_="expense")
        assert "2026-01" in totals
        assert totals["2026-01"] == 650.00

    def test_income_vs_expense(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        inc, exp, months = income_vs_expense()
        assert "2026-01" in inc
        assert inc["2026-01"] == 5000.00
        assert exp["2026-01"] == 650.00


class TestBudgetMetrics:
    def test_budget_vs_actual(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        from database.crud import set_budget

        set_budget("Food", 1, 2026, 500.00)
        results = budget_vs_actual(1, 2026)
        assert len(results) == 1
        assert results[0]["category"] == "Food"
        assert results[0]["actual"] == 200.00
        assert results[0]["percentage"] == 40.0


class TestInsights:
    def test_highest_spending_category(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        top = highest_spending_category()
        assert top == "Food" or top == "Utilities"

    def test_average_monthly_spend(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        avg = average_monthly_spend()
        assert avg > 0

    def test_savings_rate(self, db_session, sample_transactions):
        for t in sample_transactions:
            add_transaction(**t)
        rate = savings_rate()
        assert rate > 0
