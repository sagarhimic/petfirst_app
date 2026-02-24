
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.Franchises.franchise_review import FranchiseReview
from app.models.Franchises.doctor_review import DoctorReview


def add_franchise_doctor_review_service(
    franchise_id: int,
    rating: int | None,
    review_text: str | None,
    doctor_id: int | None,
    doctor_rating: int | None,
    doctor_review_text: str | None,
    user_id: int,
    db: Session
):
    try:
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
        db.flush()


        if franchise_review.review_id > 0:
            
            doctor_service_review = DoctorReview(
                review_id=franchise_review.review_id,
                franchise_id=franchise_id,
                user_id=user_id,
                doctor_id=doctor_id,
                rating=rating,
                review_text=review_text,
                review_date=datetime.utcnow()
            )
            db.add(doctor_service_review)

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
