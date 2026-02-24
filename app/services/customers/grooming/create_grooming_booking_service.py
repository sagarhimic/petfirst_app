
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from math import radians

from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_address import BookingAddress
from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails
from app.models.user_location import UserLocation
from app.utils.helpers import parse_date, parse_time, booking_type_price
from fastapi import HTTPException, Request
from app.services.customers.billing_service import create_bill_service
from app.utils.Notifications.grooming_notification import send_grooming_booking_notification
from app.utils.push_notification import push_notification

def create_grooming_booking_service(
    db: Session,
    user_id: int,
    franchise_id: int,
    data: dict
):
    try:
        # -----------------------------
        # Cart validation
        # -----------------------------
        cart = (
            db.query(GroomingCart)
            .filter(
                GroomingCart.franchise_id == franchise_id,
                GroomingCart.customer_id == user_id
            )
            .first()
        )

        if not cart:
            return {
                "status": False,
                "message": "Cart is Empty! Please add to services to Cart."
            }

        cart_ids = (
            db.query(GroomingCart.cart_id)
            .filter(
                GroomingCart.franchise_id == franchise_id,
                GroomingCart.customer_id == user_id
            )
            .all()
        )

        cart_ids = [c.cart_id for c in cart_ids]

        cart_details = (
            db.query(GroomingCartDetails)
            .filter(GroomingCartDetails.cart_id.in_(cart_ids))
            .all()
        )

        now = datetime.utcnow()

        # -----------------------------
        # Create Booking
        # -----------------------------
        booking = Bookings(
            service_type=cart.service_type,
            booking_date=now,
            booking_to=now,
            booking_time=now.time(),
            customer_id=user_id,
            pet_id=cart.pet_id,
            franchise_id=franchise_id,
            total_amount=data.get("total_amount", 0),
            discount=data.get("discount", 0),
            booking_status=1,
            gst=data.get("gst"),
            sgst=data.get("sgst"),
            service_tax=data.get("service_tax"),
            created_by=user_id,
            created_at=now
        )

        db.add(booking)
        db.flush()  # Generate booking_id

        # -----------------------------
        # Insert Booking Details
        # -----------------------------
        for item in cart_details:
            detail = BookingDetails(
                booking_id=booking.booking_id,
                service_id=item.service_id,
                booking_from=item.booking_from,
                booking_time=item.booking_time,
                amount=item.amount,
                status=1,
                created_at=now,
                created_by=user_id
            )
            db.add(detail)

        # -----------------------------
        # Insert Booking Address
        # -----------------------------
        location = (
            db.query(UserLocation)
            .filter(
                UserLocation.user_id == user_id,
                UserLocation.is_primary == 1
            )
            .first()
        )

        if location:
            address = BookingAddress(
                booking_id=booking.booking_id,
                customer_id=user_id,
                location_id=location.location_id,
                created_at=now
            )
            db.add(address)

        # -----------------------------
        # Billing
        # -----------------------------
        bill_response = create_bill_service(
            db=db,
            booking_id=booking.booking_id,
            data=data
        )

        if not bill_response["status"]:
            db.rollback()
            return {
                "status": 400,
                "error": "Bill details not created.",
                "message": "Something went wrong"
            }

        # -----------------------------
        # Delete Cart
        # -----------------------------
        db.query(GroomingCartDetails) \
            .filter(GroomingCartDetails.cart_id.in_(cart_ids)) \
            .delete(synchronize_session=False)

        db.query(GroomingCart) \
            .filter(
                GroomingCart.franchise_id == franchise_id,
                GroomingCart.customer_id == user_id
            ) \
            .delete(synchronize_session=False)

        db.commit()

        # -----------------------------
        # Notifications (Optional Hooks)
        # -----------------------------
        # Send to Franchise
        send_grooming_booking_notification(
            db,
            booking_id=booking.booking_id,
            user_type="franchise"
        )

        # Send to Customer
        send_grooming_booking_notification(
            db,
            booking_id=booking.booking_id,
            user_type="customer"
        )

        customer_noti_msg = {
            "title": f"Dear {booking.customer.name}, Grooming Service Booking Confirmed | {datetime.now().strftime('%m/%d/%Y')}",
            "desc": f"Dear {booking.customer.name} you have successfully confirmed your Grooming Service booking ID - {booking_id}"
        }

        # Push Notifications

        noti_users = [booking.user_id]

        push_notification(
            db=db,
            users=noti_users,
            send_data=customer_noti_msg,
            user_type="user"
        )

        # -----------------------------
        # Final Response
        # -----------------------------
        return {
            "status": 200,
            "booking_id": booking.booking_id,
            "data": {
                "service_type": booking.service_type,
                "booking_date": booking.booking_date,
                "booking_time": booking.booking_time,
                "customer_id": booking.customer_id,
                "pet_id": booking.pet_id,
                "franchise_id": booking.franchise_id,
                "total_amount": booking.total_amount,
                "discount": booking.discount,
                "gst": booking.gst,
                "sgst": booking.sgst,
                "service_tax": booking.service_tax
            },
            "transaction_details": bill_response["bill"],
            "service_details": bill_response["service_details"],
            "bill_details": bill_response["bill_details"],
            "message": "We have recieved your Booking details Successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
