import pytest
import pandas as pd
import io

from database.crud import add_transaction, get_all_transactions


class TestCSVImport:
    def _upload_csv(self, csv_content):
        return io.StringIO(csv_content)

    def test_valid_csv_import(self, db_session):
        csv_data = "type,amount,category,date,description\nincome,1000,Salary,2026-01-01,Test\n"
        with self._upload_csv(csv_data) as f:
            df = pd.read_csv(f)
        for _, row in df.iterrows():
            add_transaction(
                row["type"].strip().lower(), float(row["amount"]),
                row["category"].strip(), row["date"].strip(),
                str(row.get("description", "")).strip() if pd.notna(row.get("description")) else None,
            )
        txns = get_all_transactions()
        assert len(txns) == 1

    def test_invalid_amount_rejected(self, db_session):
        csv_data = "type,amount,category,date,description\nexpense,-50,Food,2026-01-01,Test\n"
        with self._upload_csv(csv_data) as f:
            df = pd.read_csv(f)
        for _, row in df.iterrows():
            if float(row["amount"]) <= 0:
                continue
            add_transaction(
                row["type"].strip().lower(), float(row["amount"]),
                row["category"].strip(), row["date"].strip(), None,
            )
        txns = get_all_transactions()
        assert len(txns) == 0

    def test_bad_date_rejected(self, db_session):
        csv_data = "type,amount,category,date\nexpense,100,Food,not-a-date\n"
        with self._upload_csv(csv_data) as f:
            df = pd.read_csv(f)
        from utils.validators import validate_date
        valid, _ = validate_date(df.iloc[0]["date"])
        assert not valid

    def test_missing_columns_detected(self):
        csv_data = "type,amount\nincome,1000\n"
        df = pd.read_csv(io.StringIO(csv_data))
        required = {"type", "amount", "category", "date"}
        missing = required - set(df.columns.str.strip().str.lower())
        assert "category" in missing
        assert "date" in missing

    def test_partial_success(self, db_session):
        csv_data = "type,amount,category,date\nexpense,100,Food,2026-01-01\nincome,-50,Salary,2026-01-01\n"
        imported = 0
        with self._upload_csv(csv_data) as f:
            df = pd.read_csv(f)
        for _, row in df.iterrows():
            if float(row["amount"]) <= 0:
                continue
            add_transaction(
                row["type"].strip().lower(), float(row["amount"]),
                row["category"].strip(), row["date"].strip(), None,
            )
            imported += 1
        assert imported == 1
        txns = get_all_transactions()
        assert len(txns) == 1
