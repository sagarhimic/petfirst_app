from fastapi import Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customers.pet_schema import ValidatePetRequest
from app.core.jwt_auth import get_auth_user_id
from app.core.database import get_db
from app.services.customers.pet_service import store_pet_service

def store_pet(
    request: ValidatePetRequest = Depends(),
    file: UploadFile | None = File(None),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return store_pet_service(db, request, file, user_id)
