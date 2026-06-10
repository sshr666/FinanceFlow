# Quickstart Validation Guide: FinanceFlow

## Prerequisites

- Python 3.11+
- pip

## Setup

```bash
# Clone and enter the project directory
cd finance-flow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

## Run the Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

## Validation Scenarios

### Scenario 1: Basic Transaction Lifecycle

1. Open the app → Dashboard loads with empty state and "Add your first transaction" prompt.
2. Navigate to **Transactions** page → Click **Add Transaction**.
3. Set type=Income, amount=1000, category=Salary, date=today → Submit.
4. Set type=Expense, amount=200, category=Food, date=today → Submit.
5. Navigate to **Dashboard** → Verify: Balance=$800, Income=$1000, Spending=$200.
6. Edit the expense transaction → change amount to 150 → Verify dashboard updates to Balance=$850.
7. Delete the expense transaction → Verify dashboard shows Balance=$1000.

**Expected**: Full CRUD lifecycle works with correct financial calculations.

### Scenario 2: Dynamic Categories

1. Navigate to **Transactions** → find category dropdown → See default categories.
2. Add a transaction with a new category name "Side Hustle" → Category is created on-the-fly.
3. Category dropdown now includes "Side Hustle".
4. Rename or delete a category (if supported via UI) → Verify all transactions in that category are updated or prompted to reassign.

**Expected**: Categories are fully dynamic; no hardcoded category list.

### Scenario 3: Analytics & Charts

1. Add transactions across multiple categories and two different months.
2. Navigate to **Analytics** → Verify category-wise chart, monthly comparison chart, and income vs expense chart render with correct data.
3. Change the date range selector → Charts update dynamically.

**Expected**: Charts render correctly and respond to filter changes (Constitution Principle VIII).

### Scenario 4: Budget Tracking

1. Navigate to **Budgets** → Create a budget for Food: limit=$500, month=current.
2. Add expense transactions in Food category totaling $400 → Verify budget shows 80% usage with alert.
3. Add more Food expenses to reach $500+ → Verify budget shows 100%+ with exceeded alert.

**Expected**: Budget alerts trigger at correct thresholds (Constitution Principle III).

### Scenario 5: CSV Import/Export

1. Navigate to **CSV Tools** → Click **Export** → CSV file downloads with all transactions.
2. Open the CSV in a text editor to verify columns: `type,amount,category,date,description`.
3. Create a test CSV with: one valid row, one row with invalid amount (-50), one row with bad date.
4. Import the test CSV → Verify valid row is imported, invalid rows are reported with specific error messages.

**Expected**: Export produces standard format; import validates per [CSV Format Contract](contracts/csv-format.md).

### Scenario 6: Empty State Handling

1. Open Dashboard with no transactions → Verify empty state UI with guidance.
2. Navigate to Analytics → Verify empty state message.
3. Navigate to Budgets → Verify empty state message.
4. Navigate to Insights → Verify empty state message.

**Expected**: Every page handles empty state gracefully (Constitution Principle III).

### Scenario 7: Environment Configuration

1. Verify `.env` file is loaded (not hardcoded).
2. Change `FINANCEFLOW_DB_PATH` in `.env` → Restart app → Database is created at new path.
3. Check no secrets or paths are visible in any Python source file.

**Expected**: Zero hardcoded values (Constitution Principle I).

## Test Commands

```bash
# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

## Deployment to Streamlit Cloud

1. Push code to a GitHub repository.
2. Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click **New app** → Select the repository and branch → Set main file to `app.py`.
4. Go to **Advanced settings** → Add secrets from `st.secrets` (no `.env` file needed on cloud).
5. Deploy.

**Note**: SQLite data on Streamlit Cloud is ephemeral. Use CSV export for regular backups.
