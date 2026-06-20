import time
from database.crud import add_transaction, get_all_transactions


class TestPerformance:
    def test_dashboard_loads_under_3s_with_500_transactions(
        self, db_session, large_transaction_set
    ):
        for t in large_transaction_set:
            add_transaction(**t)
        start = time.time()
        txns = get_all_transactions()
        elapsed = time.time() - start
        assert len(txns) == 550
        assert elapsed < 3.0, f"Dashboard load took {elapsed:.2f}s, expected <3.0s"

    def test_chart_data_fast_with_500_transactions(
        self, db_session, large_transaction_set
    ):
        for t in large_transaction_set:
            add_transaction(**t)
        from analytics.metrics import category_spending, monthly_totals

        start = time.time()
        _spending = category_spending()
        m1 = time.time()
        _totals = monthly_totals()
        m2 = time.time()
        c1 = m1 - start
        c2 = m2 - m1
        total = c1 + c2
        assert total < 2.0, f"Chart data computation took {total:.2f}s, expected <2.0s"
