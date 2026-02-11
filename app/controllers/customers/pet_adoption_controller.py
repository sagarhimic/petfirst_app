from fastapi import Depends, Request, Form, Query
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.schemas.customers.auth_schema import ValidateUserLocationRequest
from app.services.customers.pet_adoption_service import add_enquiry_service, enquiries_list_service, get_online_pets_list_service, pet_adoption_details_service
from app.schemas.customers.pet_adoption_schema import PetFilterRequest, StorePetAdoptionRequest

def add_enquiry(
    pet_adoption_id: int,
    full_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    contact_method: int = Form(...),
    time_to_contact: int = Form(...),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = StorePetAdoptionRequest(
        full_name=full_name,
        email=email,
        mobile=mobile,
        contact_method=contact_method,
        time_to_contact=time_to_contact
    )

    return add_enquiry_service(db, user_id, pet_adoption_id, data)

def enquiries_list(
    request: Request,
    search_key: str = Query("", alias="search_key"),
    status_id: str = Query("", alias="status_id"),
    date_from: str = Query("", alias="date_from"),
    date_to: str = Query("", alias="date_to"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return enquiries_list_service(
        db=db,
        user_id=user_id,
        search_key=search_key,
        status_id=status_id,
        date_from=date_from,
        date_to=date_to, request=request
    )

async def get_online_pets_list(
    latitude: str = Form(...),
    longitude: str = Form(...),
    pet_types: List[int] = Form([]),
    size: List[int] = Form([]),
    gender: List[int] = Form([]),
    breeds: List[int] = Form([]),
    colors: List[int] = Form([]),
    age: Optional[str] = Form(None),
    page: int = Form(1),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = PetFilterRequest(
        latitude=latitude,
        longitude=longitude,
        pet_types=pet_types,
        size=size,
        gender=gender,
        breeds=breeds,
        colors=colors,
        age=age,
        page=page
    )
    return get_online_pets_list_service(db, user_id, data)

def pet_adoption_details(
    pet_id: int,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return pet_adoption_details_service(
        pet_id=pet_id,
        user_id=user_id,
        db=db
    )

