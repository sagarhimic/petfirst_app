from fastapi import Depends, Request, Form
from decimal import Decimal
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.schemas.customers.auth_schema import ValidateUserLocationRequest
from app.services.customers.profile_service import get_profile_service, store_user_location_service

def get_profile(
    request: Request,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return get_profile_service(db, user_id, request)

def save_location(
    location: str = Form(...),
    location_type: int = Form(...),
    address: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    pin_code: Optional[int] = Form(None),
    is_primary: Optional[int] = Form(None),
    latitude: Decimal = Form(...),
    longitude: Decimal = Form(...),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = ValidateUserLocationRequest(
        location=location,
        location_type=location_type,
        address=address,
        country=country,
        city=city,
        state=state,
        pin_code=pin_code,
        is_primary=is_primary,
        latitude=latitude,
        longitude=longitude
    )

    return store_user_location_service(db, data, user_id)
