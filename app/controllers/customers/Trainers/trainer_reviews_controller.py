from fastapi import Depends, Form, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.Trainers.trainer_review_service import create_trainer_review, get_trainer_review_service

# Get Trainer Reviews
def get_trainer_review(
    trainer_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_trainer_review_service(
        trainer_id = trainer_id,
        db=db,
        user_id=user_id,
    )


# Add Trainer Service Review
async def store_trainer_review(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    # Read Laravel-style form-data
    form_data = dict(await request.form())

    return create_trainer_review(
        db=db,
        user_id=user_id,
        data=form_data
    )

        
