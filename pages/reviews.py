import streamlit as st

from database.reviews import add_review, get_all_reviews, get_average_rating
from config.translations import t


def render():
    st.title(t("page_title_reviews"))

    avg_rating = get_average_rating()
    all_reviews = get_all_reviews()
    total_reviews = len(all_reviews)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("reviews_average_rating"), f"{avg_rating:.1f} / 5")
    with col2:
        st.metric(t("reviews_total_reviews"), total_reviews)
    with col3:
        full = int(round(avg_rating))
        empty = 5 - full
        stars_html = "⭐" * full + "☆" * empty
        label = t("reviews_out_of", rating=f"{avg_rating:.1f}")
        st.markdown(
            f"<div style='text-align:center;font-size:1.8rem;line-height:1.2;'>{stars_html}</div>"
            f"<div style='text-align:center;color:#94a3b8;font-size:0.85rem;'>{label}</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader(t("reviews_leave"))
    with st.form("review_form", clear_on_submit=True):
        name = st.text_input(t("reviews_name"), max_chars=100)
        rating = st.selectbox(
            t("reviews_rating"),
            options=[5, 4, 3, 2, 1],
            format_func=lambda x: "⭐" * x,
        )
        comment = st.text_area(t("reviews_comment"), max_chars=500)
        st.caption(t("reviews_comment_limit"))

        if st.form_submit_button(t("reviews_submit"), type="primary", use_container_width=True):
            name = name.strip()
            comment = comment.strip()

            errors = []
            if not name:
                errors.append(t("reviews_name_required"))
            if not rating:
                errors.append(t("reviews_rating_required"))
            if not comment:
                errors.append(t("reviews_comment_required"))
            elif len(comment) > 500:
                errors.append(t("reviews_comment_too_long"))

            if errors:
                for err in errors:
                    st.error(err)
            else:
                try:
                    add_review(name, rating, comment)
                    st.success(t("reviews_success"))
                    st.rerun()
                except Exception:
                    st.error(t("reviews_error"))

    st.divider()

    st.subheader(t("reviews_recent"))

    if not all_reviews:
        st.info(t("reviews_no_reviews"))
    else:
        for r in all_reviews:
            stars = "⭐" * r.rating
            st.markdown(
                f'<div class="review-card">'
                f'<div class="review-header">'
                f'<span class="review-username">{r.username}</span>'
                f'<span class="review-date">{r.created_at}</span>'
                f"</div>"
                f'<div class="review-stars">{stars}</div>'
                f'<div class="review-comment">{r.comment}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )


render()
