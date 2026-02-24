
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.Franchises.franchise_review import FranchiseReview
from app.models.Franchises.franchise_service_review import FranchiseServiceReview


def _extract_array(data: dict, key: str):
    """
    Converts:
    service_id[0], service_id[1] → [value0, value1]
    """
    items = []
    for k, v in data.items():
        if k.startswith(f"{key}["):
            items.append(v)
    return items


def add_franchise_review_service(
    db: Session,
    user_id: int,
    data: dict
):
    try:
        franchise_id = data.get("franchise_id")
        rating = data.get("rating")
        review_text = data.get("review_text")

        if not franchise_id:
            return {
                "status": False,
                "message": "Franchise ID is required"
            }

        # -----------------------------
        # Main Franchise Review
        # -----------------------------
        franchise_review = FranchiseReview(
            user_id=user_id,
            franchise_id=franchise_id,
            rating=rating,
            review_text=review_text,
            review_date=datetime.utcnow()
        )

        db.add(franchise_review)

        # -----------------------------
        # Extract Laravel-style arrays
        # -----------------------------
        service_ids = _extract_array(data, "service_id")
        service_ratings = _extract_array(data, "service_rating")
        service_reviews = _extract_array(data, "service_review_text")

        # -----------------------------
        # Insert Service Reviews
        # -----------------------------
        for index, service_id in enumerate(service_ids):
            service_review = FranchiseServiceReview(
                user_id=user_id,
                franchise_id=franchise_id,
                service_id=service_id,
                rating=service_ratings[index] if index < len(service_ratings) else None,
                review_text=service_reviews[index] if index < len(service_reviews) else None,
                review_date=datetime.utcnow()
            )
            db.add(service_review)

        db.commit()

        return {
            "status": True,
            "message": "Review added successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
