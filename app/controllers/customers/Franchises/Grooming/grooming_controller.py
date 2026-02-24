# app/controllers/customers/franchise_controller.py

from fastapi import Depends, Query, HTTPException, Request, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.grooming.grooming_service import get_grooming_service
from app.services.customers.grooming.grooming_details_service import grooming_details_service
from app.services.customers.grooming.create_grooming_booking_service import create_grooming_booking_service
from app.services.customers.grooming.reschedule_grooming_booking_service import reschedule_grooming_booking_service
from app.services.customers.grooming.remove_grooming_service import remove_service

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
# Grooming Details
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

# Grooming Booking Create
def create_grooming_booking(
    franchise_id: int,
    total_amount: float = Form(...),
    discount: float = Form(0),
    gst: float = Form(0),
    sgst: float = Form(0),
    service_tax: float = Form(0),
    transaction_id: str = Form(...),
    payment_method: int = Form(...),
    payment_status: str = Form(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    data = {
        "total_amount": total_amount,
        "discount": discount,
        "gst": gst,
        "sgst": sgst,
        "service_tax": service_tax,
        "transaction_id": transaction_id,
        "payment_method": payment_method,
        "payment_status": payment_status
    }

    return create_grooming_booking_service(
        db=db,
        user_id=user_id,
        franchise_id=franchise_id,
        data=data
    )

# Reschedule Booking
def reschedule_grooming_booking(
    booking_id: int,
    booking_from: str = Form(...),
    booking_time: str = Form(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    data = {
        "booking_from": booking_from,
        "booking_time": booking_time
    }

    return reschedule_grooming_booking_service(
        db=db,
        user_id=user_id,
        booking_id=booking_id,
        data=data
    )

# Remove Service
def remove_grooming_service(
    service_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return remove_service(
        db=db,
        user_id=user_id,
        service_id=service_id
    )

def remove_service_by_cart_api(
    cart_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return remove_service_by_cart(
        db=db,
        user_id=user_id,
        cart_id=cart_id
    )
