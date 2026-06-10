from sqlalchemy import Column, Integer, Float, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    limit_amount = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("category", "month", "year", name="uq_budget_category_month_year"),
    )


class Settings(Base):
    __tablename__ = "settings"

    key = Column(Text, primary_key=True)
    value = Column(Text, nullable=False)
