from sqlalchemy import Column, Integer, Float, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=1)
    type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, default=1)
    category = Column(Text, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    limit_amount = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "category", "month", "year", name="uq_budget_user_category_month_year"),
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)


class Settings(Base):
    __tablename__ = "settings"

    user_id = Column(Integer, primary_key=True)
    key = Column(Text, primary_key=True)
    value = Column(Text, nullable=False)
