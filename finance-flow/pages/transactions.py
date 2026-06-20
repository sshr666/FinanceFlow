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
    validate_category,
    validate_description,
)
from utils.empty_states import show_empty_state
from config.translations import t


def render():
    st.title(t("page_title_transactions"))

    txns = get_all_transactions()
    categories = get_all_categories()

    tab1, tab2 = st.tabs([t("tab_transactions"), t("tab_manage_categories")])

    with tab1:
        _render_transaction_list(txns)

    with tab2:
        _render_category_management(categories)

    if not txns:
        show_empty_state(
            t("empty_transactions_title"),
            t("empty_transactions_message"),
            t("empty_transactions_cta"),
            t("nav_transactions"),
        )


def _render_transaction_list(txns):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(t("subheader_transaction_history"))
    with col2:
        if st.button(
            t("btn_add_transaction"), type="primary", use_container_width=True
        ):
            st.session_state.show_add_form = True

    if st.session_state.get("show_add_form") or st.session_state.get("edit_txn"):
        _render_transaction_form(txns)

    if txns:
        data = []
        for txn in txns:
            sign = "+" if txn["type"] == "income" else "-"
            amt = f"${txn['amount']:,.2f}"
            data.append(
                {
                    "Date": txn["date"],
                    "Type": t(txn["type"]).capitalize(),
                    "Category": txn["category"],
                    "Amount": f"{sign}{amt}",
                    "Description": txn["description"] or "",
                    "ID": txn["id"],
                }
            )
        st.dataframe(
            data,
            column_config={
                "ID": None,
                "Date": st.column_config.TextColumn(t("col_date"), width="small"),
                "Type": st.column_config.TextColumn(t("col_type"), width="small"),
                "Category": st.column_config.TextColumn(
                    t("col_category"), width="small"
                ),
                "Amount": st.column_config.TextColumn(t("col_amount"), width="small"),
                "Description": st.column_config.TextColumn(
                    t("col_description"), width="medium"
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        _render_edit_delete_controls(txns)


def _render_transaction_form(txns):
    editing = st.session_state.get("edit_txn")
    header = t("header_edit_transaction") if editing else t("header_add_transaction")
    with st.expander(header, expanded=True):
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            with col1:
                type_ = st.selectbox(
                    t("form_type"),
                    ["income", "expense"],
                    format_func=lambda x: t(x),
                    index=0
                    if not editing
                    else (0 if editing["type"] == "income" else 1),
                )
                amt = st.number_input(
                    t("form_amount"),
                    min_value=0.01,
                    format="%.2f",
                    value=float(editing["amount"]) if editing else 0.01,
                )
                categories = get_all_categories()

                cat_choice = st.selectbox(
                    t("form_existing_category"),
                    options=categories
                    if categories
                    else [t("no_categories_available")],
                    index=_find_category_index(categories, editing["category"])
                    if editing and categories
                    else 0,
                    disabled=not categories,
                )

                new_category = st.text_input(
                    t("form_new_category"),
                    placeholder=t("form_new_category_placeholder"),
                )

                cat_input = new_category.strip() if new_category.strip() else cat_choice

            with col2:
                date_val = st.date_input(
                    t("form_date"),
                    value=(
                        datetime.strptime(editing["date"], "%Y-%m-%d").date()
                        if editing
                        else datetime.now().date()
                    ),
                )
                desc = st.text_area(
                    t("form_description"),
                    value=editing["description"]
                    if editing and editing["description"]
                    else "",
                )

            cols = st.columns([1, 1, 2])
            with cols[0]:
                submitted = st.form_submit_button(
                    t("btn_save"), type="primary", use_container_width=True
                )
            with cols[1]:
                if st.form_submit_button(t("btn_cancel"), use_container_width=True):
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
                    st.success(t("success_transaction_updated"))
                    st.session_state.pop("edit_txn", None)
                else:
                    add_transaction(type_, amount, category, date_str, description)
                    st.success(t("success_transaction_added"))
                    st.session_state.pop("show_add_form", None)
                st.rerun()


def _render_edit_delete_controls(txns):
    st.markdown(t("quick_actions"))
    col1, col2 = st.columns(2)
    with col1:
        txn_ids = {
            f"#{txn['id']} - {txn['date']} {txn['category']} (${txn['amount']:,.2f})": txn
            for txn in txns
        }
        if txn_ids:
            selected_label = st.selectbox(
                t("select_transaction_edit_delete"), options=list(txn_ids.keys())
            )
            selected = txn_ids[selected_label]
            if st.button(t("btn_edit_selected")):
                st.session_state.edit_txn = selected
                st.rerun()
            if st.button(t("btn_delete_selected"), type="secondary"):
                st.session_state.confirm_delete = selected["id"]
                st.rerun()

    with col2:
        if st.session_state.get("confirm_delete"):
            txn_id = st.session_state.confirm_delete
            st.warning(t("confirm_delete_message", id=txn_id))
            conf_col1, conf_col2 = st.columns(2)
            with conf_col1:
                if st.button(t("btn_yes_delete"), type="primary"):
                    delete_transaction(txn_id)
                    st.session_state.pop("confirm_delete", None)
                    st.success(t("success_transaction_deleted", id=txn_id))
                    st.rerun()
            with conf_col2:
                if st.button(t("btn_no_cancel")):
                    st.session_state.pop("confirm_delete", None)
                    st.rerun()


def _find_category_index(categories, target):
    try:
        return categories.index(target)
    except ValueError:
        return 0


def _render_category_management(categories):
    st.subheader(t("subheader_categories"))
    st.caption(t("caption_categories_auto"))

    if categories:
        st.write(t("existing_categories"), ", ".join(sorted(categories)))

    with st.expander(t("expander_rename_category")):
        old = st.selectbox(
            t("select_category_to_rename"),
            options=categories if categories else [""],
            key="rename_old",
        )
        new = st.text_input(t("new_name"), key="rename_new")
        if st.button(t("btn_rename")) and old and new:
            rename_category(old, new)
            st.success(t("success_renamed", old=old, new=new))
            st.rerun()

    with st.expander(t("expander_delete_category")):
        del_cat = st.selectbox(
            t("select_category_to_delete"),
            options=categories if categories else [""],
            key="del_cat",
        )
        reassign = st.text_input(
            t("reassign_transactions"), value="Other", key="reassign_cat"
        )
        if st.button(t("btn_delete_category")) and del_cat:
            delete_category(del_cat, reassign)
            st.success(t("success_deleted_category", cat=del_cat))
            st.rerun()


render()
