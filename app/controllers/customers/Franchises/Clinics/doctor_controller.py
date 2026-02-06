# app/controllers/customers/doctor_controller.py

from fastapi import Depends, Query, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.doctor_service import get_doctors_service
from app.services.customers.doctor_details_service import doctor_details_service

def get_doctors(
    request: Request,
    franchise_id: int,
    latitude: float | None = Query(None),
    longitude: float | None = Query(None),
    search_key: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id),
):
    return get_doctors_service(
        db=db,
        request=request,
        user_id=user_id,
        franchise_id=franchise_id,
        latitude=latitude,
        longitude=longitude,
        search_key=search_key,
        page=page,
    )

# Doctor Details Info

def doctor_details(
    doctor_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id),
):
    return doctor_details_service(
        db=db,
        request=request,
        user_id=user_id,
        doctor_id=doctor_id
    )
