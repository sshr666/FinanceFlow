# FinanceFlow 💰

A personal finance tracker built with Streamlit. Manage income, expenses, budgets, and get spending insights.

## Features

- **Dashboard** — Total balance, monthly income/spending, savings overview, recent transactions
- **Transactions** — Add, edit, delete income/expense transactions with dynamic categories
- **Analytics** — Category-wise spending charts, monthly trends, income vs expense comparison
- **Budgets** — Set monthly category budgets with visual alerts at 80% and 100% thresholds
- **CSV Tools** — Export transactions to CSV, import from CSV with row-level validation
- **Insights** — Spending patterns, savings rate, trend detection, budget alerts

## Quick Start

```bash
# Clone and enter the project
git clone <repo-url>
cd finance-flow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed (defaults work out of the box)

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
finance-flow/
├── app.py                 # Streamlit entry point
├── pages/                 # UI pages
│   ├── dashboard.py
│   ├── transactions.py
│   ├── analytics.py
│   ├── budgets.py
│   ├── csv_tools.py
│   └── insights.py
├── database/              # Database layer
│   ├── models.py          # SQLAlchemy models
│   ├── crud.py            # CRUD operations
│   └── connection.py      # Engine and session
├── analytics/             # Business logic
│   ├── metrics.py         # Financial calculations
│   ├── charts.py          # Plotly chart builders
│   └── insights.py        # Spending insights
├── utils/                 # Shared utilities
│   ├── helpers.py
│   ├── validators.py
│   └── empty_states.py
├── config/                # Configuration
│   ├── settings.py        # Environment config loader
│   ├── styling.py         # UI theme
│   └── categories.py      # Default categories
├── tests/                 # Test suite
│   ├── conftest.py
│   ├── test_database.py
│   ├── test_transactions.py
│   ├── test_csv_import.py
│   ├── test_analytics.py
│   └── test_performance.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Configuration

All configuration is via environment variables (`.env` file locally, `st.secrets` on Streamlit Cloud):

| Variable | Default | Description |
|----------|---------|-------------|
| `FINANCEFLOW_DB_PATH` | `financeflow.db` | SQLite database file path |
| `FINANCEFLOW_DEFAULT_CURRENCY` | `USD` | Currency for display |
| `FINANCEFLOW_BUDGET_ALERT_THRESHOLD` | `80` | Budget alert percentage |
| `FINANCEFLOW_DEBUG` | `false` | Enable debug logging |

## Testing

```bash
cd finance-flow
pytest -v
```

Run with coverage:
```bash
pytest --cov=. --cov-report=term-missing
```

## Deployment: Streamlit Cloud

1. Push the code to a GitHub repository (include the `finance-flow/` directory).
2. Go to https://streamlit.io/cloud and click **New app**.
3. Select your repository, branch, and set the main file path to `finance-flow/app.py`.
4. In **Advanced settings**, add secrets (NOT `.env`):

   ```toml
   FINANCEFLOW_DB_PATH = "financeflow.db"
   FINANCEFLOW_DEFAULT_CURRENCY = "USD"
   FINANCEFLOW_BUDGET_ALERT_THRESHOLD = "80"
   ```

5. Click **Deploy**.

**Note**: SQLite data on Streamlit Cloud is ephemeral — it resets on each deploy. Use the CSV Export feature for regular backups.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Database**: SQLite via SQLAlchemy
- **Charts**: Plotly
- **Data**: pandas
