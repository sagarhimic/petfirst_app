from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_history_reschedule import BookingHistoryReschedule
from app.utils.helpers import parse_date, parse_time
from app.utils.Notifications.reschedule_grooming_notification import send_reschedule_grooming_booking_notification

def reschedule_grooming_booking_service(
    db: Session,
    user_id: int,
    booking_id: int,
    data: dict
):
    try:
        if not booking_id:
            return {
                "status": False,
                "message": "select Booking"
            }

        booking_from = parse_date(data.get("booking_from"))
        booking_time = parse_time(data.get("booking_time"))

        now = datetime.utcnow()

        # -----------------------------
        # Fetch previous booking detail
        # -----------------------------
        previous = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_id == booking_id)
            .first()
        )

        if not previous:
            return {
                "status": False,
                "message": "Booking not found"
            }

        # -----------------------------
        # Insert reschedule history
        # -----------------------------
        history = BookingHistoryReschedule(
            booking_id=booking_id,
            booking_from=previous.booking_from,
            booking_time=previous.booking_time
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

        if not info:
            db.rollback()
            return {
                "status": False,
                "message": "Booking not found"
            }

        booking_type_name = (
            "Tele Medicine" if info.booking_type == 1
            else "House Call" if info.booking_type == 2
            else ""
        )

        db.commit()

        # -----------------------------
        # 🔔 Notifications / SMS (HOOKS)
        # -----------------------------
        # Send to Franchise
        send_reschedule_grooming_booking_notification(
            db,
            booking_id=booking_id,
            user_type="franchise"
        )

        # Send to Customer
        send_reschedule_grooming_booking_notification(
            db,
            booking_id=booking_id,
            user_type="customer"
        )

        customer_noti_msg = {
            "title": f"Dear {booking.customer.name}, Reschedule Grooming Booking Service | {datetime.now().strftime('%m/%d/%Y')}",
            "desc": f"Dear {booking.customer.name} you have successfully Reschedule Grooming Service booking ID - {booking_id}"
        }

        # Push Notifications

        noti_users = [booking.user_id]

        push_notification(
            db=db,
            users=noti_users,
            send_data=customer_noti_msg,
            user_type="user"
        )

        return {
            "status": 200,
            "booking_id": booking_id,
            "message": "Booking Rescheduled Successfully."
        }

    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )
