import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from config.settings import get_config
from database.models import Base


def get_db_path():
    return get_config("DB_PATH", "financeflow.db")


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        db_path = get_db_path()
        _engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
        )
    return _engine


SessionFactory = None


def get_session():
    global SessionFactory
    if SessionFactory is None:
        engine = get_engine()
        SessionFactory = scoped_session(sessionmaker(bind=engine))
    return SessionFactory()


def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    _create_indexes(engine)


def _create_indexes(engine):
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type)"))
        conn.commit()
