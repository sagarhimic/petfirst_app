from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.core.database import SessionLocal

from app.schemas.customers.pet_schema import ValidatePetRequest
from app.services.customers.pet_service import save_pet_details

def store_pet_details(
    request: ValidatePetRequest,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return save_pet_details(db, user_id, request)
