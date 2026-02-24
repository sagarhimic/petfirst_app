# app/controllers/customers/doctor_controller.py

from fastapi import Depends, Query, Request, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.doctor_service import get_doctors_service
from app.services.customers.doctor_details_service import doctor_details_service
from app.services.customers.doctor_booking_service import create_doctor_booking_service
from app.services.customers.reschedule_clinic_booking_service import reschedule_clinic_booking_service
from app.services.customers.generate_time_slots_service import  generate_time_slots_service

def get_doctors(
    request: Request,
    franchise_id: int,
    latitude: float | None = Query(None),
    longitude: float | None = Query(None),
    search_key: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id),
):
    return get_doctors_service(
        db=db,
        request=request,
        user_id=user_id,
        franchise_id=franchise_id,
        latitude=latitude,
        longitude=longitude,
        search_key=search_key,
        page=page,
    )

# Doctor Details Info

def doctor_details(
    doctor_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id),
):
    return doctor_details_service(
        db=db,
        request=request,
        user_id=user_id,
        doctor_id=doctor_id
    )

# Create Doctor Booking
def create_doctor_booking(
    doctor_id: int,

    booking_type: int = Form(...),
    booking_date: str = Form(...),
    booking_time: str = Form(...),
    pet_id: int | None = Form(None),

    transaction_id: str = Form(...),
    payment_method: int = Form(...),
    payment_status: str = Form(...),

    kms: float = Form(0),

    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return create_doctor_booking_service(
        db=db,
        doctor_id=doctor_id,
        user_id=user_id,
        data={
            "booking_type": booking_type,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "pet_id": pet_id,
            "transaction_id": transaction_id,
            "payment_method": payment_method,
            "payment_status": payment_status,
            "kms": kms
        }
    )

# Reschedule Booking
def reschedule_clinic_booking(
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

    return reschedule_clinic_booking_service(
        db=db,
        user_id=user_id,
        booking_id=booking_id,
        data=data
    )

# generate Time Slots
def generate_time_slots(
    booking_type: int = Query(..., description="1 = Tele Medicine, 2 = House Call"),
    kms: float = Query(..., description="Distance in kilometers")
):
    return generate_time_slots_service(
        booking_type=booking_type,
        kms=kms
    )
