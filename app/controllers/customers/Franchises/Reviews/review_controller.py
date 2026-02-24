# app/controllers/customers/franchises/reviews_controller.py

from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.Reviews.review_service import add_franchise_review_service
from app.services.customers.Reviews.doctor_review_service import add_franchise_doctor_review_service

# Add Service Review
async def add_franchise_review(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    # Read Laravel-style form-data
    form_data = dict(await request.form())

    return add_franchise_review_service(
        db=db,
        user_id=user_id,
        data=form_data
    )

# Add Doctor Review 
async def add_franchise_Doctor_review(
    franchise_id: int = Form(...),
    rating: int = Form(None),
    review_text: str = Form(None),
    doctor_id: int = Form(...),
    doctor_rating: int = Form(None),
    doctor_review_text: str = Form(None),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return add_franchise_doctor_review_service(
        franchise_id=franchise_id,
        rating=rating,
        review_text=review_text,
        doctor_id=doctor_id,
        doctor_rating=doctor_rating,
        doctor_review_text=doctor_review_text,
        user_id=user_id,
        db=db
    )
