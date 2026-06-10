# Research: FinanceFlow Application

## Language & Runtime

- **Decision**: Python 3.11+
- **Rationale**: Streamlit requires Python 3.8+; 3.11 provides performance improvements and is the current stable baseline for Streamlit Cloud.
- **Alternatives considered**: None — Streamlit is Python-only.

## Dependencies

| Dependency | Purpose | Best Practice |
|-----------|---------|---------------|
| streamlit | Web UI framework | Use `@st.cache_data` for expensive operations; split into pages/ |
| pandas | Data manipulation for analytics and CSV | Read CSV in chunks for large imports; use DataFrame.query for filtering |
| plotly | Interactive charts | Use `plotly.express` for quick charts, `plotly.graph_objects` for custom layouts |
| sqlalchemy | ORM for SQLite | Use declarative base; connection pooling via `create_engine` with `check_same_thread=False` for Streamlit |
| python-dotenv | Load .env into environment | Load at app startup before any config read |

## Database

- **Decision**: SQLite via SQLAlchemy
- **Rationale**: Zero configuration, file-based, compatible with Streamlit Cloud ephemeral storage. SQLAlchemy provides abstraction layer for potential future migration.
- **Alternatives considered**: PostgreSQL (requires server), DuckDB (analytics-focused, less mature for transactional workloads).
- **Key considerations**: SQLite on Streamlit Cloud is ephemeral — data resets on each deploy. Use CSV export as backup mechanism.

## Project Structure

- **Decision**: pages/ + database/ + analytics/ + utils/ + config/ layout
- **Rationale**: Clean separation of concerns matching Constitution Principle II. Streamlit auto-discovers pages/ directory for multi-page apps.
- **Alternatives considered**: Monolithic single-file app (rejected — violates maintainability).

## Testing

- **Decision**: pytest with direct database operations
- **Rationale**: pytest is the standard Python testing framework. Tests should use an in-memory SQLite database for isolation.
- **Key areas**: Database CRUD operations, transaction calculations, CSV import validation, dashboard analytics aggregation.

## Deployment

- **Decision**: Streamlit Community Cloud
- **Rationale**: Free tier, direct GitHub repo connection, supports secrets management via `st.secrets`.
- **Key considerations**: Pin all dependencies in `requirements.txt`; use `st.secrets` instead of `.env` on cloud; no OS-level dependencies.
