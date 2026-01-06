from fastapi import Depends, UploadFile, File, Form
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.jwt_auth import get_auth_user_id
from app.core.database import get_db
from app.services.customers.pet_service import store_pet_service, update_pet_pic_service

def store_pet(
    pet_type: int = Form(...),
    pet_name: str = Form(...),

    age_yr: int | None = Form(None),
    age_month: int | None = Form(None),
    dob: datetime | None = Form(None),

    breed: int = Form(...),
    color: int = Form(...),

    height: float = Form(...),
    weight: int = Form(...),

    gender: int = Form(...),
    is_primary: int | None = Form(None),

    file: Optional[UploadFile] = File(None),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = {
        "pet_type": pet_type,
        "pet_name": pet_name,
        "age_yr": age_yr,
        "age_month": age_month,
        "dob": dob,
        "breed": breed,
        "color": color,
        "height": height,
        "weight": weight,
        "gender": gender,
        "is_primary": is_primary
    }

    return store_pet_service(db, data, file, user_id)

def update_pet_pic(
    pet_id: int,
    file: Optional[UploadFile] = File(...),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return update_pet_pic_service(db, pet_id, file, user_id)
