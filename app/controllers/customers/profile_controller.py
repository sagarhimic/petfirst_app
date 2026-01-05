from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.profile_service import get_profile_service

def get_profile(
    request: Request,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return get_profile_service(db, user_id, request)
