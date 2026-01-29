from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.upcoming_bookings_service import upcoming_bookings_service

def upcoming_bookings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return upcoming_bookings_service(db, user_id)
