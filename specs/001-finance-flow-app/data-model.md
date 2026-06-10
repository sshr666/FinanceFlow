# Data Model: FinanceFlow

## Entity-Relationship Overview

```
┌──────────────────┐       ┌──────────────────┐
│   Transaction    │       │     Budget       │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ type             │       │ category (FK)    │
│ amount           │       │ month            │
│ category         │       │ year             │
│ description      │       │ limit_amount     │
│ date             │       └──────────────────┘
│ created_at       │
└──────────────────┘

┌──────────────────┐
│    Settings      │
├──────────────────┤
│ key (PK)         │
│ value            │
└──────────────────┘
```

*Note: Category is a string field on Transaction (user-defined, dynamically configurable). Budget references category by name.*

---

## Transaction

Represents a single financial entry (income or expense).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | INTEGER (PK) | AUTOINCREMENT, NOT NULL | Primary key |
| type | TEXT | NOT NULL, IN ('income', 'expense') | Determines balance direction |
| amount | REAL | NOT NULL, > 0 | Always positive; sign determined by type |
| category | TEXT | NOT NULL | User-defined; dynamically configurable |
| description | TEXT | nullable, max 500 chars | Optional user note |
| date | TEXT (ISO date) | NOT NULL, format YYYY-MM-DD | Transaction date |
| created_at | TEXT (ISO datetime) | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Validation Rules**:
- `amount` MUST be > 0 (positive). Negative values are rejected.
- `type` MUST be exactly 'income' or 'expense'.
- `date` MUST be a valid calendar date in YYYY-MM-DD format.
- `category` MUST be a non-empty string.
- `description`, if provided, MUST NOT exceed 500 characters.
- `amount` stored with REAL type; rounding to 2 decimal places on write/display.

---

## Budget

Represents a monthly spending limit for a specific category.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | INTEGER (PK) | AUTOINCREMENT, NOT NULL | Primary key |
| category | TEXT | NOT NULL, UNIQUE(month, year, category) | References category by name |
| month | INTEGER | NOT NULL, 1-12 | Month of the budget |
| year | INTEGER | NOT NULL, >= 2020 | Year of the budget |
| limit_amount | REAL | NOT NULL, > 0 | Budget cap for the month |

**Validation Rules**:
- `month` MUST be between 1 and 12.
- `year` MUST be >= 2020.
- `limit_amount` MUST be > 0.
- Combination of (category, month, year) MUST be unique (one budget per category per month).
- Current spend is computed as SUM of expense transactions in matching category/month/year.

---

## Settings

Key-value store for application configuration persisted at runtime.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| key | TEXT (PK) | NOT NULL, UNIQUE | Setting identifier |
| value | TEXT | NOT NULL | Setting value (stored as string) |

**Examples**:
- `default_currency` → `"USD"`
- `savings_target` → `"500.00"`
- `budget_alert_threshold` → `"80"`

---

## Category Management

Categories are NOT a separate database table. They are:
1. Extracted dynamically from distinct `category` values in the Transaction table.
2. Initialized with a sensible default set on first run.
3. User-defined via the UI (create, rename, delete) with transaction reassignment on deletion.

**Default Categories**:
- Income: Salary, Freelance, Investments, Other Income
- Expense: Food, Housing, Transport, Entertainment, Utilities, Healthcare, Shopping, Other Expense
