import os
from dotenv import load_dotenv

load_dotenv()


CONFIG_DEFAULTS = {
    "DB_PATH": "financeflow.db",
    "DEFAULT_CURRENCY": "USD",
    "BUDGET_ALERT_THRESHOLD": "80",
    "DEBUG": "false",
}


def get_config(key, default=None):
    env_key = f"FINANCEFLOW_{key}"
    env_value = os.getenv(env_key)
    if env_value is not None:
        return env_value
    if default is not None:
        return default
    return CONFIG_DEFAULTS.get(key, default)


def get_config_int(key, default=None):
    value = get_config(key, default)
    try:
        return int(value)
    except (ValueError, TypeError):
        return int(CONFIG_DEFAULTS.get(key, 0))


def get_config_bool(key, default=None):
    value = get_config(key, default)
    return str(value).lower() in ("true", "1", "yes")
