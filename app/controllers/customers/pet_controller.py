from fastapi import Depends, Query, UploadFile, File, Form, Request
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.jwt_auth import get_auth_user_id
from app.core.database import get_db
from app.services.customers.pet_service import store_pet_service, update_pet_pic_service, pet_details_service, update_pet_service, pet_update_primary_service, edit_pet_service
from app.schemas.customers.pet_schema import UpdatePetRequest, PetUpdatePrimaryRequest

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

def get_pet_details(
    request: Request,
    search_key: Optional[str] = Query(None),
    pet_type: Optional[str] = Query(None),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    # 🔥 Normalize empty strings
    search_key = search_key.strip() if search_key else None
    pet_type = int(pet_type) if pet_type and pet_type.isdigit() else None

    return pet_details_service(db, user_id, request, search_key, pet_type)

def update_pet(
    pet_id: int,
    pet_type: int = Form(...),
    pet_name: str = Form(...),
    breed: int = Form(...),
    color: int = Form(...),
    height: float = Form(...),
    weight: int = Form(...),
    gender: int = Form(...),

    age_yr: Optional[int] = Form(None),
    age_month: Optional[int] = Form(None),
    dob: Optional[str] = Form(None),
    is_primary: Optional[int] = Form(None),

    file: Optional[UploadFile] = File(None),

    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = UpdatePetRequest(
        pet_type=pet_type,
        pet_name=pet_name,
        breed=breed,
        color=color,
        height=height,
        weight=weight,
        gender=gender,
        age_yr=age_yr,
        age_month=age_month,
        dob=dob,
        is_primary=is_primary
    )

    return update_pet_service(db, pet_id, user_id, data, file)

def pet_update_primary(
    pet_id: int = Form(...),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = PetUpdatePrimaryRequest(
        pet_id=pet_id,
    )
    return pet_update_primary_service(db, user_id, data)

def edit_pet_details(
    request: Request,
    pet_id: int,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return edit_pet_service(db, user_id, pet_id, request)

