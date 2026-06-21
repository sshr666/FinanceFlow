import streamlit as st
from config.translations import t


def show_empty_state(title, message, cta_label=None):
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"### {title}")
        st.markdown(message)

        if cta_label:
            st.info(t("use_sidebar_to_open", label=cta_label))

    st.markdown("---")
