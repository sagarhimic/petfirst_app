# app/controllers/customers/franchise_controller.py

from fastapi import Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.franchise_service import get_franchises_service

def get_franchises(
    request: Request,       
    latitude: float = Query(...),
    longitude: float = Query(...),
    search_key: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_franchises_service(
        db=db,
        request=request,
        latitude=latitude,
        longitude=longitude,
        page=page,
        search_key=search_key
    )
