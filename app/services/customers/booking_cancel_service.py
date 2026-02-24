from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.bookings import Bookings
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser


def cancel_booking_service(
    booking_id: int,
    reason_id: int,
    db: Session,
    user_id: int,
):
    try:

        if not booking_id:
            raise HTTPException(
                status_code=400,
                detail="select Booking"
            )

        # -----------------------------
        # Update booking status
        # -----------------------------
        db.query(Bookings) \
            .filter(Bookings.booking_id == booking_id) \
            .update({
                "booking_status": 3,
                "cancel_reason": reason_id,
                "updated_at": datetime.utcnow(),
                "updated_by": user_id
            })

        booking = (
            db.query(Bookings)
            .filter(Bookings.booking_id == booking_id)
            .first()
        )

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        db.commit()

        # -----------------------------
        # Trainer Notification
        # -----------------------------
        noti_msg = {
            "title": f"Cancelled - Booking | {datetime.utcnow().strftime('%m/%d/%Y')}",
            "desc": f"Customer was booking cancelled - BookingID - {booking_id}"
        }

        noti_store = Notification(
            type_id=booking.service_type,
            title=f"Booking Cancelled - {booking_id}",
            link=f"trainer/get-booking-details/{booking_id}",
            booking_id=booking_id,
            created_at=datetime.utcnow()
        )

        db.add(noti_store)
        db.flush()  # get noti_store.id

        if booking.service_type == 2 and booking.trainer_id:
            db.add(
                NotificationUser(
                    noti_id=noti_store.id,
                    trainer_id=booking.trainer_id
                )
            )
            # 🔔 call trainer push notification here if exists
            # trainer_push_notification([booking.trainer_id], noti_msg)

        # -----------------------------
        # Customer Notification
        # -----------------------------
        customer_msg = {
            "title": f"Cancelled Booking for {booking.servicetype.service_name} | {datetime.utcnow().strftime('%m/%d/%Y')}",
            "desc": f"You have Cancelled your booking. BookingID: - {booking_id}"
        }

        customer_noti = Notification(
            type_id=booking.service_type,
            title=f"Cancelled Booking for BookingID - {booking_id}",
            link=f"customer/get-booking-details/{booking_id}",
            booking_id=booking_id,
            created_at=datetime.utcnow()
        )

        db.add(customer_noti)
        db.flush()

        db.add(
            NotificationUser(
                noti_id=customer_noti.id,
                customer_id=user_id
            )
        )

        # 🔔 call customer push notification here if exists
        # push_notification([user_id], customer_msg)

        db.commit()

        return {
            "status": 200,
            "booking_id": booking_id,
            "message": "Booking Cancelled Successfully."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )
