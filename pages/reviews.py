import streamlit as st

from database.crud import add_review, get_all_reviews, delete_review
from config.translations import t


def render():
    st.title(t("page_title_reviews"))

    reviews = get_all_reviews()

    with st.expander(t("subheader_write_review"), expanded=not reviews):
        with st.form("review_form", clear_on_submit=True):
            title = st.text_input(t("form_review_title"))
            content = st.text_area(t("form_review_content"))
            rating = st.slider(t("form_rating"), 1, 5, 5)
            submitted = st.form_submit_button(t("btn_submit_review"), type="primary", use_container_width=True)
            if submitted:
                if title and content:
                    username = st.session_state.get("username", "Anonymous")
                    add_review(username, title, content, rating)
                    st.success(t("success_review_submitted"))
                    st.rerun()
                else:
                    st.warning(t("error_category_required"))

    st.subheader(t("subheader_all_reviews"))

    if not reviews:
        st.info(t("empty_reviews_message"))
        return

    user_id = st.session_state.get("user_id")

    for review in reviews:
        with st.container():
            stars = "⭐" * (review["rating"] or 0)
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"**{review['title']}** {stars}")
                st.caption(t("label_review_by", username=review["username"], date=review["created_at"][:10]))
                st.write(review["content"])
            with col2:
                if user_id and review["user_id"] == user_id:
                    if st.button(t("btn_delete_review"), key=f"del_{review['id']}"):
                        delete_review(review["id"])
                        st.rerun()
        st.divider()


render()
