import streamlit as st


def show_empty_state(title, message, cta_label=None, cta_link=None):
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"### {title}")
        st.markdown(message)

        if cta_label:
            st.info(f"👉 Use the sidebar to open {cta_label}")

    st.markdown("---")