<!--
  SYNC IMPACT REPORT
  Version change: N/A (initial template) → 1.0.0
  Modified principles: N/A (all new)
  Added sections:
    - 9 Core Principles (I-IX)
    - Technology Stack & Constraints
    - Development Workflow
    - Governance (amendment procedure, versioning policy, compliance)
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md — ⚠ pending (review "Constitution Check" gate references)
    - .specify/templates/spec-template.md — ✅ updated (no changes needed)
    - .specify/templates/tasks-template.md — ✅ updated (no changes needed)
    - .specify/templates/checklist-template.md — ✅ updated (no changes needed)
  Follow-up TODOs:
    - RATIFICATION_DATE: needs to be set to the original adoption date of this constitution
-->
# Personal Finance Tracker Constitution

## Core Principles

### I. No Hardcoded Values
- No hardcoded API keys, secrets, database paths, categories, budgets, or user data MUST appear in source code.
- All configuration MUST use environment variables and configuration files.
- Categories, budgets, and all user-facing settings MUST be dynamically configurable at runtime.

### II. Modular Architecture
- UI, database, analytics, and utility logic MUST be separated into distinct modules.
- Files MUST be kept small and single-purpose.
- Logic duplication MUST be avoided; shared logic MUST be extracted into reusable utilities.

### III. Data Integrity and Validation
- ALL transaction inputs MUST be validated before processing.
- Invalid amounts, malformed dates, and unexpected data types MUST be rejected with clear error messages.
- Empty states (no transactions, no data) MUST be handled gracefully with informative UI placeholders.

### IV. User Experience Consistency
- The UI MUST follow a minimal modern design aesthetic.
- The Streamlit layout MUST be responsive across screen sizes.
- Styling MUST be dark-mode friendly.
- Spacing, typography, and naming MUST remain consistent throughout the application.

### V. Performance
- Dashboard loading MUST be fast; optimize SQLite queries with indexes where needed.
- Streamlit rerenders MUST be minimized; use `@st.cache_data` for expensive operations.
- Avoid unnecessary recomputation of analytics or chart data on every interaction.

### VI. Maintainability
- Naming conventions MUST be clear and consistent across the codebase.
- Utility functions MUST be reusable and well-organized.
- Environment-based configuration MUST be used for all environment-specific settings.
- Comments SHOULD be used sparingly, only where logic is non-obvious or a design decision requires rationale.

### VII. Security
- Secrets MUST NEVER be exposed in source code or committed to version control.
- API keys and sensitive configuration MUST be stored in `.env` locally and loaded via `st.secrets` on Streamlit Cloud.
- CSV data imported by users MUST be sanitized and validated before processing.

### VIII. Analytics Quality
- ALL financial calculations MUST be mathematically accurate; verify rounding and summation logic.
- Charts and visualizations MUST update dynamically when transaction data changes.
- Insights and summaries MUST be generated exclusively from real (stored) transaction data, never from mock or hardcoded values.

### IX. Deployment Readiness
- The project MUST run without code changes both locally and on Streamlit Cloud.
- `requirements.txt` MUST be kept up to date with all runtime dependencies; pin major versions.

## Technology Stack & Constraints

- **Framework**: Streamlit (Python) for the UI layer.
- **Database**: SQLite for local persistence (compatible with Streamlit Cloud ephemeral storage).
- **Visualization**: Plotly for interactive financial charts.
- **Configuration**: `python-dotenv` + `.env` for local secrets; `st.secrets` for Streamlit Cloud.
- **Testing**: pytest for validation logic, analytics accuracy, and data integrity tests.
- **Dependencies**: All runtime dependencies MUST be pinned in `requirements.txt`; no OS-level dependencies beyond Python stdlib + pip.

## Development Workflow

1. All feature work MUST begin with a specification and plan review.
2. Configuration changes MUST be validated against the No Hardcoded Values principle.
3. Data validation logic MUST have corresponding test coverage.
4. UI changes MUST be reviewed for dark-mode compatibility and responsive layout.
5. Before any deployment, a full `requirements.txt` audit MUST confirm no missing or extraneous dependencies.
6. All PRs MUST verify compliance with the principles in this constitution.

## Governance

- This constitution supersedes all other development conventions and practices.
- Amendments require:
  1. A documented proposal describing the change and rationale.
  2. Approval by the project maintainer.
  3. A migration or update plan for affected code, if applicable.
- Versioning follows Semantic Versioning (MAJOR.MINOR.PATCH):
  - MAJOR: Principle removal or backward-incompatible governance change.
  - MINOR: New principle or materially expanded guidance.
  - PATCH: Clarifications, wording refinements, typo fixes.
- Every PR MUST include a "Constitution Check" verifying compliance with all applicable principles. Violations MUST be documented in the Complexity Tracking section of the plan.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-06-10
