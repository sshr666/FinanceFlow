# Configuration Schema Contract: FinanceFlow

## Environment Variables

Variables loaded from `.env` (local) or `st.secrets` (Streamlit Cloud).

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `FINANCEFLOW_DB_PATH` | No | `financeflow.db` | SQLite database file path |
| `FINANCEFLOW_DEFAULT_CURRENCY` | No | `USD` | Currency symbol for display |
| `FINANCEFLOW_BUDGET_ALERT_THRESHOLD` | No | `80` | Percentage at which budget alert triggers |
| `FINANCEFLOW_DEBUG` | No | `false` | Enable debug logging |

## .env File Format

```
FINANCEFLOW_DB_PATH=data/financeflow.db
FINANCEFLOW_DEFAULT_CURRENCY=USD
FINANCEFLOW_BUDGET_ALERT_THRESHOLD=80
FINANCEFLOW_DEBUG=false
```

## Settings Table (Runtime)

Persisted settings stored in the `settings` database table (overrides env defaults).

| Key | Default | Description |
|-----|---------|-------------|
| `default_currency` | `USD` | Currency symbol for display (from env or setting) |
| `savings_target` | `0` | Monthly savings target amount |
| `budget_alert_threshold` | `80` | Override for budget alert threshold |

## Resolution Order

1. `settings` table value (if set)
2. Environment variable (if set)
3. Hardcoded default (as documented above)

*No secrets, paths, or user data are ever hardcoded.*
