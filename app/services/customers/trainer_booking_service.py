from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.trainers.trainer_cart import TrainerCart
from app.models.trainers.trainer_cart_details import TrainerCartDetails
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_address import BookingAddress
from app.models.user_location import UserLocation
from app.models.booking_trans import BookingTransaction
from app.models.booking_history_reschedule import BookingHistoryReschedule
from app.services.customers.billing_service import create_bill_service
from app.utils.helpers import parse_date, parse_time 
from app.utils.Notifications.trainer_booking_notification import send_booking_notification
from app.utils.Notifications.trainer_reschedule_booking_notification import send_reschedule_booking_notification


def create_booking_service(
    db: Session,
    user_id: int,
    data
):
    try:
        # -----------------------------
        # Cart validation
        # -----------------------------
        cart = (
            db.query(TrainerCart)
            .filter(TrainerCart.customer_id == user_id)
            .first()
        )

        if not cart:
            return {
                "status": False,
                "message": "Cart is Empty! Please add to services to Cart."
            }

        cart_ids = (
            db.query(TrainerCart.cart_id)
            .filter(TrainerCart.customer_id == user_id)
            .all()
        )
        cart_ids = [c.cart_id for c in cart_ids]

        cart_details = (
            db.query(TrainerCartDetails)
            .filter(TrainerCartDetails.cart_id.in_(cart_ids))
            .all()
        )

        print("DEBUG cart:", cart_details)

        now = datetime.utcnow()

        # -----------------------------
        # Booking insert
        # -----------------------------
        booking = Bookings(
            service_type=cart.service_type,
            booking_date=now,
            booking_to=now,
            booking_time=now.time(),
            customer_id=user_id,
            pet_id=cart.pet_id,
            trainer_id=cart.trainer_id,
            total_amount=data.get("total_amount"),
            discount=data.get("discount", 0),
            booking_status=1,
            gst=data.get("gst"),
            sgst=data.get("sgst"),
            service_tax=data.get("service_tax"),
            created_by=user_id,
            created_at=now
        )

        db.add(booking)
        db.flush()  # booking_id generated

        print("DEBUG booking_id after flush:", booking.booking_id)
        print("DEBUG data:", data)

        # -----------------------------
        # Booking details
        # -----------------------------
        booking_details_rows = []

        for item in cart_details:
            booking_details_rows.append(
                BookingDetails(
                    booking_id=booking.booking_id,
                    service_id=item.service_id,
                    booking_from=item.booking_from,
                    booking_to=item.booking_to,
                    booking_time=item.booking_time,
                    amount=item.amount,
                    status=1,
                    created_at=now,
                    created_by=user_id
                )
            )

        if booking_details_rows:
            db.add_all(booking_details_rows)

        # -----------------------------
        # Booking address
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
        # Billing
        # -----------------------------
        bill_response = create_bill_service(
            db=db,
            booking_id=booking.booking_id,
            data=data
        )

        print("DEBUG bill_response:", bill_response)

        if not bill_response["status"]:
            db.rollback()
            return {
                "status": 400,
                "error": "Bill details not created.",
                "message": "Something went wrong"
            }

        # -----------------------------
        # Clear cart
        # -----------------------------
        db.query(TrainerCartDetails) \
            .filter(TrainerCartDetails.cart_id.in_(cart_ids)) \
            .delete(synchronize_session=False)

        db.query(TrainerCart) \
            .filter(TrainerCart.customer_id == user_id) \
            .delete(synchronize_session=False)

        db.commit()

        # -----------------------------
        # Notifications (hooks)
        # -----------------------------
        # TrainerBelNotify(booking.booking_id)
        # customerBelNotify(booking.booking_id, user_id)

        # For Trainer
        send_booking_notification(db, booking_id=booking.booking_id, user_type="trainer")
        # For Customer
        send_booking_notification(db, booking_id=booking.booking_id, user_type="customer")

        

        return {
            "status": 200,
            "booking_id": booking.booking_id,
            "data": {
                "service_type": booking.service_type,
                "booking_date": booking.booking_date,
                "booking_time": booking.booking_time,
                "customer_id": booking.customer_id,
                "pet_id": booking.pet_id,
                "trainer_id": booking.trainer_id,
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


def reschedule_trainer_booking_service(
    db: Session,
    user_id: int,
    data: dict
):
    try:
        booking_id = data.get("booking_id")

        if not booking_id:
            return {
                "status": False,
                "message": "select Booking"
            }

        booking_from = parse_date(data.get("booking_from"))
        booking_to   = parse_date(data.get("booking_to"))
        booking_time = parse_time(data.get("booking_time"))

        now = datetime.utcnow()

        db.begin()

        # -----------------------------
        # Fetch previous booking
        # -----------------------------
        previous_detail = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_id == booking_id)
            .first()
        )

        if not previous_detail:
            db.rollback()
            return {
                "status": False,
                "message": "Booking not found"
            }

        # -----------------------------
        # Insert history
        # -----------------------------
        history = BookingHistoryReschedule(
            booking_id=booking_id,
            booking_from=previous_detail.booking_from,
            booking_to=previous_detail.booking_to,
            booking_time=previous_detail.booking_time
        )
        db.add(history)

        # -----------------------------
        # Update booking details
        # -----------------------------
        updated = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_id == booking_id)
            .update(
                {
                    "booking_from": booking_from,
                    "booking_to": booking_to,
                    "booking_time": booking_time,
                    "updated_at": now,
                    "updated_by": user_id
                },
                synchronize_session=False
            )
        )

        if updated > 0:
            (
                db.query(Bookings)
                .filter(Bookings.booking_id == booking_id)
                .update(
                    {"sub_status_id": 1},
                    synchronize_session=False
                )
            )

        info = (
            db.query(Bookings)
            .filter(Bookings.booking_id == booking_id)
            .first()
        )

        db.commit()

        # -----------------------------
        # Notifications (HOOKS)
        # -----------------------------
        # trainerPushNotification(...)
        # customerPushNotification(...)
        # SMS sending hooks

        # For Trainer
        send_reschedule_booking_notification(db, booking_id=booking_id, user_type="trainer")
        # For Customer
        send_reschedule_booking_notification(db, booking_id=booking_id, user_type="customer")

        return {
            "status": 200,
            "booking_id": booking_id,
            "message": "Booking Rescheduled Successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )