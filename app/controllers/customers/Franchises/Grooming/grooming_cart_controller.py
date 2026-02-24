from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.grooming.grooming_cart_service import add_cart
from app.services.customers.grooming.grooming_cart_details_service import cart_details
from app.services.customers.grooming.grooming_cart_clear_service import clear_cart, remove_service_by_cart
from app.services.customers.grooming.modify_grooming_cart_service import modify_service_by_cart



def add_cart_grooming(
    service_type: int = Form(...),
    pet_id: int = Form(...),
    franchise_id: int = Form(...),

    service_id: List[int] = Form(...),
    booking_from: List[str] = Form(...),
    booking_time: List[str] = Form(...),

    total_amount: float = Form(0),

    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return add_cart(
        db=db,
        user_id=user_id,
        service_type=service_type,
        pet_id=pet_id,
        franchise_id=franchise_id,
        service_id=service_id,
        booking_from=booking_from,
        booking_time=booking_time,
        total_amount=total_amount
    )

# Get Grooming Cart Details
def get_cart_details(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return cart_details(db=db, user_id=user_id)

# Clear Grooming Cart 
def clear_cart_api(
    franchise_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return clear_cart(
        db=db,
        user_id=user_id,
        franchise_id=franchise_id
    )

# Remove Cart By Service
def remove_service_by_cart_api(
    cart_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return remove_service_by_cart(
        cart_id=cart_id,
        db=db,
        user_id=user_id
    )

# MOdify Grooming Booking Service
def modify_service_by_cart_api(
    cart_id: int,
    booking_from: str = Form(None),
    booking_time: str = Form(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return modify_service_by_cart(
        db=db,
        user_id=user_id,
        cart_id=cart_id,
        booking_from=booking_from,
        booking_time=booking_time
    )
