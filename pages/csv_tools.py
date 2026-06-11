import streamlit as st
import pandas as pd
import io

from database.crud import get_all_transactions, add_transaction
from utils.validators import validate_csv_row
from utils.empty_states import show_empty_state


def render():
    st.title("📁 CSV Tools")

    txns = get_all_transactions()

    tab1, tab2 = st.tabs(["Export", "Import"])

    with tab1:
        _render_export(txns)

    with tab2:
        _render_import()

    if not txns:
        show_empty_state(
            "No transactions to export",
            "Add some transactions first, then return here to export them as CSV.",
            "Go to Transactions",
            "/Transactions",
        )


def _render_export(txns):
    st.subheader("Export Transactions")
    st.caption("Download all your transactions as a CSV file.")

    if txns:
        df = pd.DataFrame(txns)
        df = df[["type", "amount", "category", "date", "description"]]
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="financeflow_transactions.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
        st.success(f"Ready to export {len(txns)} transactions.")
    else:
        st.info("No transactions to export.")


def _render_import():
    st.subheader("Import Transactions")
    st.caption("Upload a CSV file to import transactions.")
    st.markdown("**Expected columns:** `type, amount, category, date, description`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            st.error("Could not read the CSV file. Please check the format.")
            return

        required_cols = {"type", "amount", "category", "date"}
        missing = required_cols - set(df.columns.str.strip().str.lower())
        if missing:
            st.error(f"Missing required columns: {', '.join(sorted(missing))}")
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
                        description=str(row.get("description", "")).strip() if pd.notna(row.get("description")) else None,
                    )
                    imported += 1
                except Exception as e:
                    errors.append({"row": idx + 2, "errors": f"Database error: {e}"})

        st.success(f"✅ Successfully imported {imported} transactions.")
        if errors:
            st.warning(f"⚠️ {len(errors)} row(s) had errors:")
            for e in errors:
                st.markdown(f"- Row {e['row']}: {e['errors']}")

        if imported > 0:
            st.rerun()

render()