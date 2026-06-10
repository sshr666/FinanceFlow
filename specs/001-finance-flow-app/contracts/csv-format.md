# CSV Import/Export Contract: FinanceFlow

## Export Format

Exported CSV uses the following columns (header row required):

```
type,amount,category,date,description
income,1000.00,Salary,2026-06-01,Monthly salary
expense,200.00,Food,2026-06-02,Groceries
```

### Column Specifications

| Column | Type | Required | Constraints |
|--------|------|----------|-------------|
| type | string | YES | Must be exactly `income` or `expense` (case-insensitive) |
| amount | number | YES | Must be a positive number (> 0); up to 2 decimal places |
| category | string | YES | Must be non-empty |
| date | string | YES | Must be a valid date in YYYY-MM-DD format |
| description | string | NO | Free text; max 500 characters |

### Export Rules

- Exported file includes ALL transactions (no date filtering).
- Columns appear in the order above.
- No id or created_at columns are exported (these are internal).
- Character encoding: UTF-8.

## Import Format

Import follows the same column structure as export.

### Import Rules

- Fails if header row is missing or has incorrect column names.
- Fails if any REQUIRED column is missing.
- Rows with validation errors are SKIPPED (not imported) and reported to the user with row number and specific error message.
- Valid rows within the same file ARE imported even if some rows fail.
- Duplicate detection: no automatic deduplication (same data imported twice creates duplicate rows).
- Date format MUST be YYYY-MM-DD. Alternate formats are rejected with a per-row error.
