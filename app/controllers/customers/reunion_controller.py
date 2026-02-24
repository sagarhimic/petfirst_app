from fastapi import Depends, Request, Form, UploadFile, File
from decimal import Decimal
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.schemas.customers.auth_schema import ValidateUserLocationRequest
from app.services.customers.reunion_service import get_pet_parent_service, add_pet_parent_service, edit_pet_parent_service, update_pet_parent_service, delete_pet_parent_service  
from app.schemas.customers.pet_parent_schema import StorePetParentRequest, UpdatePetParentRequest


def get_pet_parent(
    request: Request,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return get_pet_parent_service(db, user_id, request)

def add_pet_parent(
    pet_id: int = Form(...),
    pet_parent_name=Form(...),
    parent_owner_name=Form(...),
    parent_mobile=Form(...),
    parent_email=Form(...),
    address=Form(...),
    state_id=Form(...),
    city=Form(...),
    country_id=Form(...),
    pincode=Form(...),
    parent_type: int = Form(...),
   
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):

    data = StorePetParentRequest(
        pet_id=pet_id,
        pet_parent_name=pet_parent_name,
        parent_owner_name=parent_owner_name,
        parent_mobile=parent_mobile,
        parent_email=parent_email,
        address=address,
        state_id=state_id,
        city=city,
        country_id=country_id,
        pincode=pincode,
        parent_type=parent_type
    )

    return add_pet_parent_service(db, user_id, data)

def edit_pet_parent(
    pet_parent_id: int,
    request: Request,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
 return edit_pet_parent_service(db, user_id, pet_parent_id, request)   

def update_pet_parent(
    pet_parent_id: int,
    pet_id: int = Form(...),
    pet_parent_name=Form(...),
    parent_owner_name=Form(...),
    parent_mobile=Form(...),
    parent_email=Form(...),
    address=Form(...),
    state_id=Form(...),
    city=Form(...),
    country_id=Form(...),
    pincode=Form(...),
    parent_type: int = Form(...),

    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):

    data = UpdatePetParentRequest(
        pet_id=pet_id,
        pet_parent_name=pet_parent_name,
        parent_owner_name=parent_owner_name,
        parent_mobile=parent_mobile,
        parent_email=parent_email,
        address=address,
        state_id=state_id,
        city=city,
        country_id=country_id,
        pincode=pincode,
        parent_type=parent_type
    )

    return update_pet_parent_service(db, user_id, pet_parent_id, data)


def delete_pet_parent(
    pet_parent_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return delete_pet_parent_service(db, user_id, pet_parent_id)