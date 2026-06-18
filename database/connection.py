import os
import sys
import logging
import tempfile
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from config.settings import get_config, resolve_db_path
from database.models import Base

logger = logging.getLogger(__name__)


_DATA_DIR = None


def _get_writable_dir():
    global _DATA_DIR
    if _DATA_DIR is None:
        _DATA_DIR = Path(tempfile.gettempdir()) / "financeflow"
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
    return _DATA_DIR


def get_db_path():
    raw = get_config("DB_PATH", "financeflow.db")
    resolved = Path(resolve_db_path(raw))
    parent = resolved.parent

    def _is_writable(path):
        return path.exists() and os.access(str(path), os.W_OK)

    if _is_writable(parent) and (_is_writable(resolved) or not resolved.exists()):
        if not resolved.exists():
            parent.mkdir(parents=True, exist_ok=True)
        return str(resolved)

    if resolved.exists():
        logger.warning("DB not writable at: %s (parent writable=%s, file writable=%s)",
                       resolved, _is_writable(parent), _is_writable(resolved))
    else:
        logger.warning("DB parent not writable at: %s (parent writable=%s)",
                       parent, _is_writable(parent))

    fallback = _get_writable_dir() / "financeflow.db"
    logger.warning("Redirecting database to writable location: %s", fallback)
    return str(fallback)


def _ensure_db_directory(db_path):
    parent = Path(db_path).parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        return True, None
    except OSError as e:
        return False, str(e)


def _log_db_diagnostics(db_path):
    p = Path(db_path)
    logger.info("=== Database Diagnostics ===")
    logger.info("Resolved DB path: %s", db_path)
    logger.info("File exists: %s", p.exists())
    if p.exists():
        logger.info("File size: %s bytes", p.stat().st_size)
        logger.info("File writable: %s", os.access(str(p), os.W_OK))
    logger.info("Parent dir: %s", p.parent)
    logger.info("Parent dir exists: %s", p.parent.exists())
    logger.info("Parent dir writable: %s", os.access(str(p.parent), os.W_OK) if p.parent.exists() else False)
    logger.info("CWD: %s", os.getcwd())
    logger.info("Project root: %s", Path(__file__).resolve().parent.parent)
    logger.info("Database is writable")


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        db_path = get_db_path()
        ok, err = _ensure_db_directory(db_path)
        if not ok:
            logger.error("Cannot create database directory: %s", err)
            fallback = _get_writable_dir() / "financeflow.db"
            logger.warning("Falling back to temp location: %s", fallback)
            db_path = str(fallback)
            _ensure_db_directory(db_path)
        _log_db_diagnostics(db_path)
        _engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
        )
    return _engine


def check_db_writable():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS _writable_test (id INTEGER)"))
            conn.execute(text("INSERT INTO _writable_test (id) VALUES (1)"))
            conn.execute(text("DELETE FROM _writable_test"))
            conn.execute(text("DROP TABLE IF EXISTS _writable_test"))
            conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)


SessionFactory = None


def get_session():
    global SessionFactory
    if SessionFactory is None:
        engine = get_engine()
        SessionFactory = scoped_session(sessionmaker(bind=engine))
    return SessionFactory()


def table_exists(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
            {"name": table_name},
        )
        return result.fetchone() is not None


def column_exists(engine, table, column):
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table})"))
        return any(row[1] == column for row in result.fetchall())


def index_exists(engine, index_name):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='index' AND name=:name"),
            {"name": index_name},
        )
        return result.fetchone() is not None


SCHEMA_VERSION_KEY = "schema_version"
SCHEMA_VERSION_VALUE = "2"


def _get_schema_version(engine):
    try:
        if not column_exists(engine, "settings", "user_id"):
            return "0"
        if table_exists(engine, "settings"):
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT value FROM settings WHERE key=:key AND user_id=0"),
                    {"key": SCHEMA_VERSION_KEY},
                )
                row = result.fetchone()
                if row:
                    return row[0]
        return "0"
    except Exception:
        return "0"


def _upgrade_schema(engine):
    version = _get_schema_version(engine)
    if version == SCHEMA_VERSION_VALUE:
        return

    try:
        with engine.begin() as conn:
            if table_exists(engine, "transactions") and not column_exists(engine, "transactions", "user_id"):
                try:
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1"))
                except Exception as e:
                    if "duplicate column" not in str(e).lower():
                        logger.warning("Could not add user_id to transactions: %s", e)

            if table_exists(engine, "budgets") and not column_exists(engine, "budgets", "user_id"):
                try:
                    conn.execute(text("ALTER TABLE budgets ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1"))
                except Exception as e:
                    if "duplicate column" not in str(e).lower():
                        logger.warning("Could not add user_id to budgets: %s", e)

            if table_exists(engine, "settings") and not column_exists(engine, "settings", "user_id"):
                try:
                    conn.execute(text("ALTER TABLE settings ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0"))
                except Exception as e:
                    if "duplicate column" not in str(e).lower():
                        logger.warning("Could not add user_id to settings: %s", e)

            if table_exists(engine, "budgets") and column_exists(engine, "budgets", "user_id"):
                try:
                    conn.execute(text(
                        "CREATE UNIQUE INDEX IF NOT EXISTS idx_budget_user_cat_month_year "
                        "ON budgets(user_id, category, month, year)"
                    ))
                except Exception as e:
                    logger.warning("Could not create idx_budget_user_cat_month_year: %s", e)

            if table_exists(engine, "transactions") and column_exists(engine, "transactions", "user_id"):
                try:
                    conn.execute(text(
                        "CREATE INDEX IF NOT EXISTS idx_transactions_user_id "
                        "ON transactions(user_id)"
                    ))
                except Exception as e:
                    logger.warning("Could not create idx_transactions_user_id: %s", e)

            if table_exists(engine, "settings") and column_exists(engine, "settings", "user_id"):
                try:
                    conn.execute(
                        text("INSERT OR IGNORE INTO settings (user_id, key, value) VALUES (0, :key, :value)"),
                        {"key": SCHEMA_VERSION_KEY, "value": SCHEMA_VERSION_VALUE},
                    )
                except Exception as e:
                    logger.warning("Could not record schema version: %s", e)
    except Exception as e:
        logger.warning("Schema upgrade failed: %s", e)


def _create_indexes(engine):
    try:
        with engine.connect() as conn:
            if table_exists(engine, "transactions"):
                for idx_col in ["date", "category", "type"]:
                    if column_exists(engine, "transactions", idx_col):
                        idx_name = f"idx_transactions_{idx_col}"
                        if not index_exists(engine, idx_name):
                            try:
                                conn.execute(text(
                                    f"CREATE INDEX IF NOT EXISTS {idx_name} ON transactions({idx_col})"
                                ))
                            except Exception as e:
                                logger.warning("Could not create %s: %s", idx_name, e)

            if table_exists(engine, "settings") and column_exists(engine, "settings", "user_id"):
                if not index_exists(engine, "idx_settings_user_id"):
                    try:
                        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_settings_user_id ON settings(user_id)"))
                    except Exception as e:
                        logger.warning("Could not create idx_settings_user_id: %s", e)

            conn.commit()
    except Exception as e:
        logger.warning("Index creation failed: %s", e)


def init_db():
    engine = get_engine()
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.warning("Could not create tables: %s", e)
    _upgrade_schema(engine)
    _create_indexes(engine)
    writable, err = check_db_writable()
    if not writable:
        logger.critical("Database is NOT WRITABLE: %s. All write operations will fail!", err)
