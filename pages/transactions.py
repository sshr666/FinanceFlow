import streamlit as st
from datetime import datetime

from database.crud import (
    add_transaction,
    update_transaction,
    delete_transaction,
    get_all_transactions,
    get_all_categories,
    rename_category,
    delete_category,
)
from utils.validators import (
    validate_amount,
    validate_date,
    validate_transaction_type,
    validate_category,
    validate_description,
)
from utils.empty_states import show_empty_state


def render():
    st.title("💳 Transactions")

    txns = get_all_transactions()
    categories = get_all_categories()

    tab1, tab2 = st.tabs(["Transactions", "Manage Categories"])

    with tab1:
        _render_transaction_list(txns)

    with tab2:
        _render_category_management(categories)

    if not txns:
        show_empty_state(
            "No transactions yet",
            "Start tracking your finances by adding your first transaction.",
            "Add a Transaction",
            "/Transactions",
        )


def _render_transaction_list(txns):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Transaction History")
    with col2:
        if st.button("➕ Add Transaction", type="primary", use_container_width=True):
            st.session_state.show_add_form = True

    if st.session_state.get("show_add_form") or st.session_state.get("edit_txn"):
        _render_transaction_form(txns)

    if txns:
        data = []
        for t in txns:
            sign = "+" if t["type"] == "income" else "-"
            amt = f"${t['amount']:,.2f}"
            data.append(
                {
                    "Date": t["date"],
                    "Type": t["type"].capitalize(),
                    "Category": t["category"],
                    "Amount": f"{sign}{amt}",
                    "Description": t["description"] or "",
                    "ID": t["id"],
                }
            )
        st.dataframe(
            data,
            column_config={
                "ID": None,
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Amount": st.column_config.TextColumn("Amount", width="small"),
                "Description": st.column_config.TextColumn("Description", width="medium"),
            },
            hide_index=True,
            use_container_width=True,
        )

        _render_edit_delete_controls(txns)


def _render_transaction_form(txns):
    editing = st.session_state.get("edit_txn")
    header = "Edit Transaction" if editing else "Add Transaction"
    with st.expander(header, expanded=True):
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            with col1:
                type_ = st.selectbox(
                    "Type",
                    ["income", "expense"],
                    index=0 if not editing else (0 if editing["type"] == "income" else 1),
                )
                amt = st.number_input(
                    "Amount",
                    min_value=0.01,
                    format="%.2f",
                    value=float(editing["amount"]) if editing else 0.01,
                )
                cat_input = st.selectbox(
                    "Category",
                    options=get_all_categories(),
                    index=_find_category_index(get_all_categories(), editing["category"]) if editing else 0,
                )
            with col2:
                date_val = st.date_input(
                    "Date",
                    value=(
                        datetime.strptime(editing["date"], "%Y-%m-%d").date()
                        if editing
                        else datetime.now().date()
                    ),
                )
                desc = st.text_area(
                    "Description (optional)",
                    value=editing["description"] if editing and editing["description"] else "",
                )

            cols = st.columns([1, 1, 2])
            with cols[0]:
                submitted = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with cols[1]:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.pop("show_add_form", None)
                    st.session_state.pop("edit_txn", None)
                    st.rerun()

            if submitted:
                valid, msg = validate_amount(amt)
                if not valid:
                    st.error(msg)
                    return
                amount = msg

                valid, msg = validate_date(date_val.strftime("%Y-%m-%d"))
                if not valid:
                    st.error(msg)
                    return
                date_str = msg

                valid, msg = validate_category(cat_input)
                if not valid:
                    st.error(msg)
                    return
                category = msg

                valid, msg = validate_description(desc)
                if not valid:
                    st.error(msg)
                    return
                description = msg if msg else None

                if editing:
                    update_transaction(
                        editing["id"],
                        type_=type_,
                        amount=amount,
                        category=category,
                        date=date_str,
                        description=description,
                    )
                    st.success("Transaction updated!")
                    st.session_state.pop("edit_txn", None)
                else:
                    add_transaction(type_, amount, category, date_str, description)
                    st.success("Transaction added!")
                    st.session_state.pop("show_add_form", None)
                st.rerun()


def _render_edit_delete_controls(txns):
    st.markdown("### Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        txn_ids = {f"#{t['id']} - {t['date']} {t['category']} (${t['amount']:,.2f})": t for t in txns}
        if txn_ids:
            selected_label = st.selectbox("Select transaction to edit/delete", options=list(txn_ids.keys()))
            selected = txn_ids[selected_label]
            if st.button("✏️ Edit Selected"):
                st.session_state.edit_txn = selected
                st.rerun()
            if st.button("🗑️ Delete Selected", type="secondary"):
                st.session_state.confirm_delete = selected["id"]
                st.rerun()

    with col2:
        if st.session_state.get("confirm_delete"):
            txn_id = st.session_state.confirm_delete
            st.warning(f"Are you sure you want to delete transaction #{txn_id}?")
            conf_col1, conf_col2 = st.columns(2)
            with conf_col1:
                if st.button("✅ Yes, Delete", type="primary"):
                    delete_transaction(txn_id)
                    st.session_state.pop("confirm_delete", None)
                    st.success(f"Transaction #{txn_id} deleted.")
                    st.rerun()
            with conf_col2:
                if st.button("❌ Cancel"):
                    st.session_state.pop("confirm_delete", None)
                    st.rerun()


def _find_category_index(categories, target):
    try:
        return categories.index(target)
    except ValueError:
        return 0


def _render_category_management(categories):
    st.subheader("Categories")
    st.caption("Categories are automatically collected from your transactions.")

    if categories:
        st.write("**Existing categories:**", ", ".join(sorted(categories)))

    with st.expander("Rename Category"):
        old = st.selectbox("Select category to rename", options=categories if categories else [""], key="rename_old")
        new = st.text_input("New name", key="rename_new")
        if st.button("Rename") and old and new:
            rename_category(old, new)
            st.success(f"Renamed '{old}' to '{new}'")
            st.rerun()

    with st.expander("Delete Category"):
        del_cat = st.selectbox("Select category to delete", options=categories if categories else [""], key="del_cat")
        reassign = st.text_input("Reassign transactions to category", value="Other", key="reassign_cat")
        if st.button("Delete Category") and del_cat:
            delete_category(del_cat, reassign)
            st.success(f"Deleted category '{del_cat}'")
            st.rerun()

render()