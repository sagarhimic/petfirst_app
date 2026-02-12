# app/controllers/customers/franchise_controller.py

from fastapi import Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.grooming.grooming_service import get_grooming_service
from app.services.customers.grooming.grooming_details_service import grooming_details_service

def get_grooming(
    request: Request,
    latitude: float | None = Query(None),
    longitude: float | None = Query(None),
    search_key: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_grooming_service(
        db=db,
        request=request,
        user_id=user_id,
        latitude=latitude,
        longitude=longitude,
        page=page,
        search_key=search_key
    )

def grooming_details(
    franchise_id: int,
    package_type: int | None = Query(None),
    search_key: str | None = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id),
    request: Request = None
):
    return grooming_details_service(
        db=db,
        franchise_id=franchise_id,
        user_id=user_id,
        package_type=package_type,
        search_key=search_key,
        request=request
    )
