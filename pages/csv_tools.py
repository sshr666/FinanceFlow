import streamlit as st
import pandas as pd
import io
from sqlalchemy import text

from database.connection import get_engine
from database.crud import get_all_transactions, add_transaction
from utils.validators import validate_csv_row
from utils.empty_states import show_empty_state
from config.translations import t


def _check_db_writable():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS _writable_test (id INTEGER)"))
            conn.execute(text("INSERT INTO _writable_test (id) VALUES (1)"))
            conn.execute(text("DELETE FROM _writable_test"))
            conn.execute(text("DROP TABLE IF EXISTS _writable_test"))
            conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)


def render():
    st.title(t("page_title_csv_tools"))

    txns = get_all_transactions()

    tab1, tab2 = st.tabs([t("tab_export"), t("tab_import")])

    with tab1:
        _render_export(txns)

    with tab2:
        _render_import()

    if not txns:
        show_empty_state(
            t("empty_csv_title"),
            t("empty_csv_message"),
            t("empty_csv_cta"),
            t("nav_transactions"),
        )


def _render_export(txns):
    st.subheader(t("subheader_export"))
    st.caption(t("caption_export"))

    if txns:
        df = pd.DataFrame(txns)
        df = df[["type", "amount", "category", "date", "description"]]
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label=t("btn_download_csv"),
            data=csv_data,
            file_name="financeflow_transactions.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
        st.success(t("success_export_ready", count=len(txns)))
    else:
        st.info(t("info_no_transactions_export"))


def _render_import():
    st.subheader(t("subheader_import"))
    st.caption(t("caption_import"))
    st.markdown(t("expected_columns"))

    uploaded_file = st.file_uploader(t("file_uploader_label"), type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            st.error(t("error_csv_read"))
            return

        required_cols = {"type", "amount", "category", "date"}
        missing = required_cols - set(df.columns.str.strip().str.lower())
        if missing:
            st.error(t("error_missing_columns", columns=", ".join(sorted(missing))))
            return

        writable, write_err = _check_db_writable()
        if not writable:
            st.error(
                f"Database is not writable: {write_err}. Cannot import transactions. "
                f"Please check file permissions or contact support."
            )
            return

        df.columns = df.columns.str.strip().str.lower()
        imported = 0
        errors = []

        for idx, row in df.iterrows():
            row_errors = validate_csv_row(row)
            if row_errors:
                errors.append({"row": idx + 2, "errors": "; ".join(row_errors)})
            else:
                try:
                    add_transaction(
                        type=row["type"].strip().lower(),
                        amount=float(row["amount"]),
                        category=row["category"].strip(),
                        date=row["date"].strip(),
                        description=str(row.get("description", "")).strip()
                        if pd.notna(row.get("description"))
                        else None,
                    )
                    imported += 1
                except Exception as e:
                    errors.append(
                        {"row": idx + 2, "errors": t("label_database_error", error=e)}
                    )

        st.success(t("success_imported", count=imported))
        if errors:
            st.warning(t("warning_import_errors", count=len(errors)))
            for e in errors:
                st.markdown(
                    t("label_import_error_row", row=e["row"], errors=e["errors"])
                )

        if imported > 0:
            st.rerun()


render()
