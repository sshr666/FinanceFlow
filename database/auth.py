import hashlib
import secrets
from datetime import datetime

from database.connection import get_session
from database.models import User
from config.translations import t


def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${h}"


def _check_password(password, stored):
    try:
        salt, h = stored.split("$", 1)
        return _hash_password(password, salt) == stored
    except (ValueError, AttributeError):
        return False


def signup(username, password):
    if not username or not username.strip():
        return None, t("error_username_required")
    if not password or len(password) < 4:
        return None, t("error_password_length")

    session = get_session()
    try:
        existing = session.query(User).filter(User.username == username.strip()).first()
        if existing:
            return None, t("error_username_exists")
        user = User(
            username=username.strip(),
            password_hash=_hash_password(password),
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        session.add(user)
        session.commit()
        return user.id, None
    finally:
        session.close()


def login(username, password):
    if not username or not password:
        return None, t("error_credentials_required")

    session = get_session()
    try:
        user = session.query(User).filter(User.username == username.strip()).first()
        if user is None:
            return None, t("error_invalid_credentials")
        if not _check_password(password, user.password_hash):
            return None, t("error_invalid_credentials")
        return user.id, None
    finally:
        session.close()
