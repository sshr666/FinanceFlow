from datetime import datetime

from database.connection import get_session
from database.models import Review


def add_review(username, rating, comment):
    session = get_session()
    try:
        review = Review(
            username=username,
            rating=rating,
            comment=comment,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        session.add(review)
        session.commit()
        return review.id
    finally:
        session.close()


def get_reviews(limit=10, offset=0):
    session = get_session()
    try:
        reviews = (
            session.query(Review)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            {
                "id": r.id,
                "username": r.username,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": r.created_at,
            }
            for r in reviews
        ]
    finally:
        session.close()


def get_all_reviews():
    session = get_session()
    try:
        return (
            session.query(Review)
            .order_by(Review.created_at.desc())
            .all()
        )
    finally:
        session.close()


def get_average_rating():
    session = get_session()
    try:
        rows = session.query(Review.rating).all()
        if not rows:
            return 0.0
        ratings = [r[0] for r in rows]
        return sum(ratings) / len(ratings)
    finally:
        session.close()
