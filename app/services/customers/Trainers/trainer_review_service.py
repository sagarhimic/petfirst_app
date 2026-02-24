from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends, Request, HTTPException
from app.models.trainer_review import TrainerReview
from app.models.trainers.trainer_service_reviews import TrainerServiceReview
from app.utils.helpers import format_date


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


def create_trainer_review(
    db: Session,
    user_id: int,
    data: dict
):
    try:
        trainer_id = data.get("trainer_id")
        rating = data.get("rating")
        review_text = data.get("review_text")

        if not trainer_id:
            return {
                "status": False,
                "message": "Franchise ID is required"
            }

        # -----------------------------
        # Main Trainer Review
        # -----------------------------
        trainer_review = TrainerReview(
            user_id=user_id,
            trainer_id=trainer_id,
            rating=rating,
            review_text=review_text,
            review_date=datetime.utcnow()
        )

        db.add(trainer_review)

        print(trainer_review.review_id)

        # -----------------------------
        # Extract Laravel-style arrays
        # -----------------------------
        service_ids = _extract_array(data, "service_id")
        service_ratings = _extract_array(data, "service_rating")
        service_reviews = _extract_array(data, "service_review_text")

        # -----------------------------
        # Insert Trainer Service Reviews
        # -----------------------------
        for index, service_id in enumerate(service_ids):
            trainer_service_review = TrainerServiceReview(
                user_id=user_id,
                trainer_id=trainer_id,
                service_id=service_id,
                rating=service_ratings[index] if index < len(service_ratings) else None,
                review_text=service_reviews[index] if index < len(service_reviews) else None,
                review_date=datetime.utcnow()
            )
            db.add(trainer_service_review)

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


# Get Trainer Service Reviews

def get_trainer_review_service(
    trainer_id: int,
    db: Session,
    user_id: int,
):
    try:
        results = (
            db.query(TrainerServiceReview)
            .filter(TrainerServiceReview.trainer_id == trainer_id)
            .all()
        )

        reviews = []
        for res in results:
            reviews.append({
                "service": res.service.service_name if res.service else None,
                "rating": res.rating,
                "review_text": res.review_text,
                "review_date": format_date(res.review_date) if res.review_date else None,
            })

        return {
            "status": True,
            "data": reviews,
            "message": "Reviews Info."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

