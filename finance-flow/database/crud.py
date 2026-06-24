import streamlit as st
from datetime import datetime

from database.connection import get_session
from database.models import Transaction, Budget, Settings


def _current_user_id():
    return st.session_state.get("user_id", 0)


def get_all_transactions():
    user_id = _current_user_id()
    session = get_session()
    try:
        txns = (
            session.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.date.desc(), Transaction.id.desc())
            .all()
        )
        return [
            {
                "id": t.id,
                "user_id": t.user_id,
                "type": t.type,
                "amount": t.amount,
                "category": t.category,
                "description": t.description,
                "date": t.date,
                "created_at": t.created_at,
            }
            for t in txns
        ]
    finally:
        session.close()


def get_transaction_by_id(txn_id):
    user_id = _current_user_id()
    session = get_session()
    try:
        t = (
            session.query(Transaction)
            .filter(Transaction.id == txn_id, Transaction.user_id == user_id)
            .first()
        )
        if t is None:
            return None
        return {
            "id": t.id,
            "user_id": t.user_id,
            "type": t.type,
            "amount": t.amount,
            "category": t.category,
            "description": t.description,
            "date": t.date,
            "created_at": t.created_at,
        }
    finally:
        session.close()


def add_transaction(type, amount, category, date, description=None):
    user_id = _current_user_id()
    session = get_session()
    try:
        txn = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            category=category,
            description=description,
            date=date,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        session.add(txn)
        session.commit()
        _clear_cache()
        return txn.id
    finally:
        session.close()


def update_transaction(
    txn_id, type_=None, amount=None, category=None, date=None, description=None
):
    user_id = _current_user_id()
    session = get_session()
    try:
        txn = (
            session.query(Transaction)
            .filter(Transaction.id == txn_id, Transaction.user_id == user_id)
            .first()
        )
        if txn is None:
            return False
        if type_ is not None:
            txn.type = type_
        if amount is not None:
            txn.amount = amount
        if category is not None:
            txn.category = category
        if date is not None:
            txn.date = date
        if description is not None:
            txn.description = description
        session.commit()
        _clear_cache()
        return True
    finally:
        session.close()


def delete_transaction(txn_id):
    user_id = _current_user_id()
    session = get_session()
    try:
        txn = (
            session.query(Transaction)
            .filter(Transaction.id == txn_id, Transaction.user_id == user_id)
            .first()
        )
        if txn is None:
            return False
        session.delete(txn)
        session.commit()
        _clear_cache()
        return True
    finally:
        session.close()


def rename_category(old_name, new_name):
    user_id = _current_user_id()
    session = get_session()
    try:
        session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.category == old_name,
        ).update({Transaction.category: new_name})
        session.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == old_name,
        ).update({Budget.category: new_name})
        session.commit()
        _clear_cache()
    finally:
        session.close()


def delete_category(name, reassign_to=None):
    user_id = _current_user_id()
    session = get_session()
    try:
        target = reassign_to if reassign_to else "Other"
        session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.category == name,
        ).update({Transaction.category: target})
        session.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == name,
        ).delete()
        session.commit()
        _clear_cache()
    finally:
        session.close()


def set_budget(category, month, year, limit_amount):
    user_id = _current_user_id()
    session = get_session()
    try:
        existing = (
            session.query(Budget)
            .filter(
                Budget.user_id == user_id,
                Budget.category == category,
                Budget.month == month,
                Budget.year == year,
            )
            .first()
        )
        if existing:
            existing.limit_amount = limit_amount
        else:
            b = Budget(
                user_id=user_id,
                category=category,
                month=month,
                year=year,
                limit_amount=limit_amount,
            )
            session.add(b)
        session.commit()
        _clear_cache()
    finally:
        session.close()


def get_budgets(month=None, year=None):
    user_id = _current_user_id()
    session = get_session()
    try:
        query = session.query(Budget).filter(Budget.user_id == user_id)
        if month is not None:
            query = query.filter(Budget.month == month)
        if year is not None:
            query = query.filter(Budget.year == year)
        budgets = query.all()
        return [
            {
                "id": b.id,
                "user_id": b.user_id,
                "category": b.category,
                "month": b.month,
                "year": b.year,
                "limit_amount": b.limit_amount,
            }
            for b in budgets
        ]
    finally:
        session.close()


def delete_budget(budget_id):
    user_id = _current_user_id()
    session = get_session()
    try:
        b = (
            session.query(Budget)
            .filter(Budget.id == budget_id, Budget.user_id == user_id)
            .first()
        )
        if b:
            session.delete(b)
            session.commit()
            _clear_cache()
            return True
        return False
    finally:
        session.close()


def get_setting(key, default=None):
    user_id = _current_user_id()
    session = get_session()
    try:
        s = (
            session.query(Settings)
            .filter(Settings.user_id == user_id, Settings.key == key)
            .first()
        )
        return s.value if s else default
    finally:
        session.close()


def set_setting(key, value):
    user_id = _current_user_id()
    session = get_session()
    try:
        existing = (
            session.query(Settings)
            .filter(Settings.user_id == user_id, Settings.key == key)
            .first()
        )
        if existing:
            existing.value = value
        else:
            s = Settings(user_id=user_id, key=key, value=value)
            session.add(s)
        session.commit()
        _clear_cache()
    finally:
        session.close()


def _clear_cache():
    pass
