# app/routers/customers/bookings.py
from fastapi import Depends, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.booking_service import get_customer_bookings

def get_bookings(
    search_key: Optional[str] = Form(None),
    status_id: Optional[List[int]] = Form(None),
    booking_from: Optional[str] = Form(None),
    booking_to: Optional[str] = Form(None),
    booking_type: Optional[int] = Form(None),
    page: int = Form(1),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_customer_bookings(
        db=db,
        user_id=user_id,
        search_key=search_key,
        status_id=status_id,
        booking_from=booking_from,
        booking_to=booking_to,
        booking_type=booking_type,
        page=page
    )
