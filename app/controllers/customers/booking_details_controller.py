from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.booking_details_service import booking_details_service

def get_booking_details(
    booking_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return booking_details_service(db, user_id, booking_id)
