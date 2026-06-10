# UI Page Contracts: FinanceFlow

## Page: Dashboard (`pages/dashboard.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/` (main page) |
| **Purpose** | Overview of financial health at a glance |
| **Displays** | Total balance, monthly income, monthly spending, savings overview, recent transactions list, spending trend chart |
| **Inputs** | None (read-only view on load) |
| **Actions** | Click transaction to navigate to edit; click "Add Transaction" button |
| **Empty state** | Welcome message with "Add your first transaction" CTA button |
| **Refresh** | Auto-updates on page load; data re-read from database |

---

## Page: Transactions (`pages/transactions.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/Transactions` |
| **Purpose** | Full transaction management |
| **Displays** | Filterable/sortable transaction table with all fields |
| **Inputs** | Add form: type (income/expense), amount, category (dropdown), date, description |
| **Actions** | Add transaction, edit inline, delete with confirmation, filter by date range / category |
| **Empty state** | "No transactions yet — add one to get started" message |
| **Validation** | Amount > 0 (reject negative/zero); date valid; category required |

---

## Page: Analytics (`pages/analytics.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/Analytics` |
| **Purpose** | Visual financial analysis |
| **Displays** | Category-wise spending pie/bar chart, monthly income vs expense bar chart, monthly comparison charts, budget usage visualization |
| **Inputs** | Month/date range selector (default: current month) |
| **Actions** | Change time range; charts update dynamically |
| **Empty state** | "Add transactions to see analytics" when no data |

---

## Page: Budgets (`pages/budgets.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/Budgets` |
| **Purpose** | Define and monitor spending limits |
| **Displays** | Budget list per category: limit, current spend, percentage, remaining; visual progress bars; alert badges |
| **Inputs** | Add budget form: category, month/year, limit amount |
| **Actions** | Create budget, edit limit, delete budget |
| **Alerts** | Visual indicator (color change / warning icon) at 80% usage; explicit alert at 100%+ |
| **Empty state** | "No budgets set — create one to track spending limits" |

---

## Page: CSV Tools (`pages/csv_tools.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/CSV Tools` |
| **Purpose** | Import/export transaction data |
| **Displays** | Export button, import file uploader, import results summary |
| **Inputs** | File upload (CSV); download trigger |
| **Actions** | Export all transactions as CSV; upload and import CSV |
| **Import validation** | Required columns: type, amount, category, date; optional: description. Invalid rows reported with specific errors. Valid rows imported, invalid rows skipped. |
| **Export format** | Columns: id, type, amount, category, description, date, created_at |

---

## Page: Insights (`pages/insights.py`)

| Contract | Detail |
|----------|--------|
| **Route** | `/Insights` |
| **Purpose** | AI/rule-based spending insights |
| **Displays** | Highest spending category, average monthly spend, spending trend, month-over-month comparison, savings rate |
| **Inputs** | Time period selector (3mo, 6mo, 12mo, all) |
| **Actions** | Change time period → insights recalculate |
| **Empty state** | "Track transactions for at least one month to see insights" |
