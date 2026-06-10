---
description: "Implementation tasks for FinanceFlow personal finance tracker"
---

# Tasks: FinanceFlow Application

**Input**: Design documents from `specs/001-finance-flow-app/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included in the Polish phase as cross-cutting verification. Each user story phase includes manual validation via the Independent Test.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `finance-flow/` at repository root (per plan.md)
- Pages: `finance-flow/pages/`
- Database: `finance-flow/database/`
- Analytics: `finance-flow/analytics/`
- Utilities: `finance-flow/utils/`
- Config: `finance-flow/config/`
- Tests: `finance-flow/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project folder structure per plan.md (`finance-flow/pages/`, `database/`, `analytics/`, `utils/`, `config/`, `tests/`)
- [x] T002 [P] Create `requirements.txt` with pinned dependencies: streamlit, pandas, plotly, sqlalchemy, python-dotenv
- [x] T003 [P] Create `.env.example` with documented variables: FINANCEFLOW_DB_PATH, FINANCEFLOW_DEFAULT_CURRENCY, FINANCEFLOW_BUDGET_ALERT_THRESHOLD, FINANCEFLOW_DEBUG
- [x] T004 [P] Create `.gitignore` for Python (`.venv/`, `__pycache__/`, `.env`, `*.db`, `.streamlit/secrets.toml`)
- [x] T005 Create `pyproject.toml` with project metadata, Python 3.11+ requirement, and basic pytest configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create SQLAlchemy database models (Transaction, Budget, Settings) in `database/models.py` per data-model.md
- [x] T007 [P] Create database engine and session management in `database/connection.py` with `check_same_thread=False` for Streamlit
- [x] T008 Create CRUD operations for Transaction (add, get, get_all, update, delete, get_by_date_range, get_by_category) in `database/crud.py`
- [x] T009 [P] Create CRUD operations for Budget (set, get, get_all, update, delete, get_by_month_year) in `database/crud.py`
- [x] T010 [P] Create CRUD operations for Settings (get, set, get_all) in `database/crud.py`
- [x] T011 [P] Create reusable helper utilities in `utils/helpers.py` (format_currency, parse_date, get_current_month_year, filter_transactions)
- [x] T012 [P] Create input validation utilities in `utils/validators.py` (validate_amount, validate_date, validate_transaction_type, validate_category)
- [x] T013 Create environment configuration loader in `config/settings.py` (load from .env, provide defaults for all config keys)
- [x] T014 [P] Create Streamlit entry point `app.py` with sidebar navigation linking to all pages (Dashboard, Transactions, Analytics, Budgets, CSV Tools, Insights), page title, and layout config
- [x] T015 [P] Create shared Streamlit styling and theme configuration in `config/styling.py` (dark-mode-friendly CSS, consistent spacing, responsive layout wrappers)
- [x] T016 Create empty state handler utility in `utils/empty_states.py` (reusable function to display consistent "no data" message with guidance)
- [x] T017 [P] Create SQLite indexes on transactions.date and transactions.category in `database/connection.py` to optimize dashboard and analytics query performance per Constitution V
- [x] T018 [P] Add `@st.cache_data` caching decorators to expensive functions in `database/crud.py` (get_all_transactions, get_by_date_range, get_by_category, dashboard aggregation queries) to minimize Streamlit rerender overhead per Constitution V

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Core Transaction Management & Dashboard (Priority: P1) 🎯 MVP

**Goal**: Users can add income/expense transactions with dynamic categories, edit/delete them, and see a dashboard with balance, income, spending, recent transactions, and spending trend.

**Independent Test**: User adds an income ($1000, Salary) and an expense ($200, Food), sees both in recent transactions, and verifies dashboard shows Balance=$800, Income=$1000, Spending=$200.

- [x] T019 [P] [US1] Create transactions page `pages/transactions.py` with add transaction form (type, amount, category, date, description fields)
- [x] T020 [US1] Implement edit transaction functionality in `pages/transactions.py` — populate form with existing transaction data on row selection
- [x] T021 [US1] Implement delete transaction with confirmation dialog in `pages/transactions.py`
- [x] T022 [P] [US1] Implement dynamic category extraction and management in `config/categories.py` (get_categories, add_category, rename_category, delete_category with transaction reassignment)
- [x] T023 [P] [US1] Create dashboard page `pages/dashboard.py` with metric cards (total balance, monthly income, monthly spending) using st.metric
- [x] T024 [US1] Add recent transactions table (last 10, newest first) to dashboard in `pages/dashboard.py`
- [x] T025 [US1] Add savings calculation (income - expenses) to dashboard in `pages/dashboard.py` with display
- [x] T026 [US1] Add input validation on transaction form (amount > 0, valid YYYY-MM-DD date, non-empty category) in `pages/transactions.py`
- [x] T027 [US1] Handle empty states on dashboard (welcome message with "Add your first transaction" CTA) and transactions page ("No transactions yet" with guidance)
- [x] T028 [US1] Add spending trend line chart (daily expenses over current month) to dashboard using Plotly in `analytics/charts.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Analytics & Budget Management (Priority: P2)

**Goal**: Users can view category-wise spending charts, monthly trends, income vs expense comparisons, budget utilization charts, set monthly category budgets, monitor usage with progress bars, and receive alerts at 80%/100% thresholds.

**Independent Test**: User navigates to Analytics, sees charts render with correct data; sets a $500 Food budget in Budgets, adds $400 in Food expenses, sees 80% alert.

- [x] T029 [P] [US2] Create metrics computation module `analytics/metrics.py` (category_spending, monthly_totals, income_vs_expense, budget_vs_actual)
- [x] T030 [P] [US2] Create Plotly chart builder functions in `analytics/charts.py` (pie_chart, bar_chart, line_chart, comparison_chart, progress_chart) — depends on T028 (same file, extend don't overwrite)
- [x] T031 [US2] Create analytics page `pages/analytics.py` with category-wise spending pie/bar chart
- [x] T032 [US2] Add monthly income vs expense grouped bar chart to `pages/analytics.py`
- [x] T033 [US2] Add monthly spending trend line chart (multi-month) to `pages/analytics.py`
- [x] T034 [P] [US2] Create budgets page `pages/budgets.py` with add/edit budget form (category, month/year, limit amount)
- [x] T035 [US2] Add budget usage progress bars (limit, current spend, remaining, percentage) to `pages/budgets.py`
- [x] T036 [US2] Implement budget warning system in `pages/budgets.py` — color change at 80%, explicit alert at 100%+
- [x] T037 [US2] Add budget utilization visualization (actual vs budget bar chart) to analytics page `pages/analytics.py`
- [x] T038 [US2] Handle empty states on analytics page ("Add transactions to see analytics") and budgets page ("No budgets set")

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Data Management, Savings & Insights (Priority: P3)

**Goal**: Users can export/import CSV data with validation, set savings targets, view progress, and see automatically generated spending insights (highest category, averages, trends, budget alerts).

**Independent Test**: User exports transactions to CSV, imports a new CSV with mixed valid/invalid rows, sets a $500 savings target, views generated insights.

- [x] T039 [P] [US3] Create CSV tools page `pages/csv_tools.py` with export button (downloads all transactions as CSV via st.download_button)
- [x] T040 [US3] Add CSV import with file upload (st.file_uploader) and row processing in `pages/csv_tools.py`
- [x] T041 [P] [US3] Create CSV row validation in `utils/validators.py` (check required columns, validate type/amount/date per row, report row-level errors)
- [x] T042 [US3] Display CSV import results (rows imported count, rows failed with per-row error messages) in `pages/csv_tools.py`
- [x] T043 [P] [US3] Create insights generation engine `analytics/insights.py` (highest_spending_category, average_monthly_spend, month_over_month_change, savings_rate, spending_trend_direction)
- [x] T044 [US3] Create insights page `pages/insights.py` with spending pattern cards and trend indicators
- [x] T045 [US3] Add savings target setting (st.number_input) and progress display (saved vs target) to insights page `pages/insights.py`
- [x] T046 [US3] Add budget alert summary (list of categories exceeding or approaching budget) to insights page `pages/insights.py`
- [x] T047 [US3] Handle empty states on CSV tools page ("No transactions to export") and insights page ("Track transactions for at least one month to see insights")

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Deployment readiness, testing, code quality improvements, and performance validation

- [x] T048 [P] Audit all source files for hardcoded values — verify every path/secret/key uses config/settings.py or env vars
- [x] T049 [P] Verify `requirements.txt` has all runtime dependencies and no dev-only packages
- [x] T050 [P] Add Streamlit Cloud deployment instructions to `README.md` (GitHub repo setup, st.secrets, deploy from branch)
- [x] T051 Create test configuration `tests/conftest.py` with in-memory SQLite engine, test session fixtures, and sample transaction factory
- [x] T052 [P] Write database CRUD tests in `tests/test_database.py` (create transaction, update, delete, constraint violations, budget uniqueness)
- [x] T053 [P] Write transaction calculation tests in `tests/test_transactions.py` (balance math, multi-transaction summation, edit recalculation, delete recalculation)
- [x] T054 [P] Write CSV validation tests in `tests/test_csv_import.py` (valid row, invalid amount, bad date, missing columns, partial success with mixed rows)
- [x] T055 [P] Write analytics computation tests in `tests/test_analytics.py` (category sums, monthly totals, budget vs actual, savings calculation)
- [x] T056 Review all files for dead code, unused imports, naming consistency, and comment quality — clean up per Constitution Principle VI
- [x] T057 Run `quickstart.md` validation scenarios end-to-end and fix any issues found
- [x] T058 [P] Create performance test fixture in `tests/conftest.py` that seeds 500+ transactions across multiple categories and months to enable dashboard load and chart responsiveness validation
- [x] T059 [P] Write performance validation tests in `tests/test_performance.py` that verify dashboard loads and analytics charts render within SC-002 (<3s with 500 transactions) and SC-006 (<2s chart update) targets using the seeded fixture

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires US1 transaction data but is independently testable with seeded data
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires US1 transaction data but is independently testable with seeded data

### Within Each User Story

- Models before services
- Services before pages/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models/tasks within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different developers
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "T019 [P] [US1] Create transactions page pages/transactions.py"
Task: "T022 [P] [US1] Dynamic category management in config/categories.py"
Task: "T023 [P] [US1] Create dashboard page pages/dashboard.py with metric cards"
```

```bash
# Launch remaining US1 tasks after parallel tasks complete:
Task: "T020 [US1] Edit transaction in pages/transactions.py"
Task: "T021 [US1] Delete transaction in pages/transactions.py"
Task: "T024 [US1] Recent transactions table in pages/dashboard.py"
Task: "T025 [US1] Savings calculation on dashboard"
Task: "T026 [US1] Input validation on transaction form"
Task: "T027 [US1] Empty states on dashboard and transactions"
Task: "T028 [US1] Spending trend chart on dashboard"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Transaction Management & Dashboard)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Add income transaction → verify dashboard balance/income updates
   - Add expense transaction → verify dashboard balance/spending updates
   - Edit transaction → verify metrics recalculate
   - Delete transaction → verify metrics update
   - Add new category → verify dropdown includes it
   - View empty state on fresh database → verify guidance message
5. Deploy to Streamlit Cloud if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Transaction Management & Dashboard)
   - Developer B: User Story 2 (Analytics & Budget Management)
   - Developer C: User Story 3 (CSV, Savings & Insights)
3. Stories complete and integrate independently
4. Team collaborates on Phase 6 (Polish) together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (for test tasks T051-T055, T058-T059)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All environment configuration MUST use `config/settings.py` — no direct os.getenv in page/analytics code (Constitution Principle I)
- All database access MUST go through `database/crud.py` — no raw SQLAlchemy queries in page code (Constitution Principle II)
