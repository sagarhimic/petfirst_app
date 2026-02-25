
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from math import radians

from app.models.Franchises.doctor_info import DoctorInfo
from app.models.Franchises.doctor import Doctor
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_address import BookingAddress
from app.models.user_location import UserLocation
from app.utils.helpers import parse_date, parse_time, booking_type_price
from fastapi import HTTPException, Request
from app.services.customers.billing_service import create_bill_service
from app.utils.Notifications.clinic_notification import send_clinic_booking_notification

def create_doctor_booking_service(
    db: Session,
    doctor_id: int,
    user_id: int,
    data: dict
):
    try:
        booking_date = parse_date(data["booking_date"])
        booking_time = parse_time(data["booking_time"])

        doctor_info = (
            db.query(DoctorInfo)
            .filter(DoctorInfo.doctor_id == doctor_id)
            .first()
        )

        franchise_user = (
            db.query(Doctor)
            .filter(Doctor.id == doctor_id)
            .first()
        )

        if not doctor_info:
            return {
                "status": False,
                "message": "Data is not available."
            }

        # -----------------------------
        # AMOUNT CALCULATION
        # -----------------------------

        result = booking_type_price(
            data["booking_type"],
            data["kms"]
        )

        # Handle Not Serviceable case
        if result == "Not Serviceable":
            return {
                "status": False,
                "message": "Service not available for this distance"
            }

        base_price = result["price"]

        gst = base_price * 0.18
        sgst = base_price * 0.18
        service_tax = base_price * 0.05

        total_amount = base_price + gst + sgst + service_tax

        now = datetime.utcnow()

        # -----------------------------
        # CREATE BOOKING
        # -----------------------------
        booking = Bookings(
            service_type=5,
            booking_type=data["booking_type"],
            franchise_id=franchise_user.franchise_id,
            booking_date=booking_date,
            booking_time=booking_time,
            customer_id=user_id,
            pet_id=data.get("pet_id"),
            doctor_id=doctor_id,
            total_amount=total_amount,
            discount=0,
            booking_status=1,
            gst=gst,
            sgst=sgst,
            service_tax=service_tax,
            created_by=user_id,
            created_at=now
        )

        db.add(booking)
        db.flush()   # booking_id generated

        # -----------------------------
        # BOOKING DETAILS
        # -----------------------------
        booking_detail = BookingDetails(
            booking_id=booking.booking_id,
            booking_from=booking_date,
            booking_time=booking_time,
            amount=doctor_info.consultation_fee,
            status=1,
            created_at=now,
            created_by=user_id
        )
        db.add(booking_detail)

        # -----------------------------
        # BOOKING ADDRESS
        # -----------------------------
        location = (
            db.query(UserLocation)
            .filter(UserLocation.user_id == user_id)
            .filter(UserLocation.is_primary == 1)
            .first()
        )

        if location:
            db.add(
                BookingAddress(
                    booking_id=booking.booking_id,
                    customer_id=user_id,
                    location_id=location.location_id,
                    created_at=now
                )
            )

        # -----------------------------
        # BILLING
        # -----------------------------
        bill_response = create_bill_service(
            db=db,
            booking_id=booking.booking_id,
            data={
                "transaction_id": data["transaction_id"],
                "total_amount": total_amount,
                "payment_method": data["payment_method"],
                "payment_status": data["payment_status"]
            }
        )

        if not bill_response["status"]:
            db.rollback()
            return {
                "status": 400,
                "error": "Bill details not created.",
                "message": "Something went wrong"
            }

        db.commit()

        # Send to Doctor
        send_clinic_booking_notification(
            db,
            booking_id=booking.booking_id,
            user_type="doctor",
            booking_type=data["booking_type"]
        )

        # Send to Customer
        send_clinic_booking_notification(
            db,
            booking_id=booking.booking_id,
            user_type="customer",
            booking_type=data["booking_type"]
        )

        # Push Notifications
        
        customer_noti_msg = {
            "title": f"Dear {booking.customer.name}, Clinic Booking Confirmed | {datetime.now().strftime('%m/%d/%Y')}",
            "desc": f"Dear {booking.customer.name} you have successfully confirmed Doctor Service booking ID - {booking_id}"
        }

        noti_users = [booking.user_id]

        push_notification(
            db=db,
            users=noti_users,
            send_data=customer_noti_msg,
            user_type="user"
        )

        return {
            "status": 200,
            "booking_id": booking.booking_id,
            "data": {
                "service_type": 5,
                "booking_type": data["booking_type"],
                "booking_date": booking_date,
                "booking_time": booking_time,
                "doctor_id": doctor_id,
                "total_amount": total_amount,
                "gst": gst,
                "sgst": sgst,
                "service_tax": service_tax
            },
            "transaction_details": bill_response["bill"],
            "service_details": bill_response["service_details"],
            "bill_details": bill_response["bill_details"],
            "message": "We have recieved your Booking details Successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
