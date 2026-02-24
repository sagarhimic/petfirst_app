from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.Franchises.Events.events import Event
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from app.services.customers.billing_service import create_bill_service


def create_event_booking_service(
    db: Session,
    event_id: int,
    user_id: int,
    data: dict
):
    try:
        # -----------------------------------
        # Get Event
        # -----------------------------------
        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        pet_id = data.get("pet_id")

        if not pet_id:
            return {
                "status": False,
                "message": "Select Pet"
            }

        # -----------------------------------
        # Tax Calculation (Laravel equivalent)
        # -----------------------------------
        CGST = 9
        SGST = 9
        SERVICE_TAX = 5

        entry_fee = float(event.entry_fee or 0)

        cgst = (entry_fee * CGST) / 100
        sgst = (entry_fee * SGST) / 100
        service_tax = (entry_fee * SERVICE_TAX) / 100

        total_amount = entry_fee + cgst + sgst + service_tax

        data["total_amount"] = total_amount

        # -----------------------------------
        # Booking master
        # -----------------------------------
        booking = Bookings(
            service_type=7,
            booking_date=datetime.utcnow(),
            booking_to=datetime.utcnow(),
            booking_time=datetime.utcnow().time(),
            customer_id=user_id,
            pet_id=pet_id,
            total_amount=total_amount,
            discount=0,
            booking_status=1,
            gst=cgst,
            sgst=sgst,
            service_tax=service_tax,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(booking)
        db.flush()  # get booking_id

        # -----------------------------------
        # Booking details
        # -----------------------------------
        booking_detail = BookingDetails(
            booking_id=booking.booking_id,
            event_id=event_id,
            booking_from=event.event_date,
            booking_to=event.event_date,
            booking_time=booking.booking_time,
            amount=entry_fee,
            status=1,
            created_at=datetime.utcnow(),
            created_by=user_id
        )

        db.add(booking_detail)

        # -----------------------------------
        # Create Bill
        # -----------------------------------
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
                "error_message": bill_response,
                "message": "Something went wrong"
            }

        # -----------------------------------
        # Confirmation Data
        # -----------------------------------
        confirm_event_details = {
            "event_name": event.name,
            "event_date": event.event_date,
            "event_time_from": event.event_time_from,
            "event_time_to": event.event_time_to,
            "location": event.location,
            "state": event.state.name if event.state else None,
            "country": event.country.name if event.country else None
        }

        # -----------------------------------
        # Notifications (simplified)
        # -----------------------------------
        notification = Notification(
            type_id=7,
            customer_id=user_id,
            title=f"Customer Booked an Event - {booking.booking_id}",
            link=f"customer/get-booking-details/{booking.booking_id}",
            booking_id=booking.booking_id,
            created_at=datetime.utcnow()
        )

        db.add(notification)
        db.flush()

        notification_user = NotificationUser(
            noti_id=notification.id,
            customer_id=user_id
        )

        db.add(notification_user)

        db.commit()

        return {
            "status": 200,
            "booking_id": booking.booking_id,
            "data": {
                "service_type": 7,
                "total_amount": total_amount,
                "gst": cgst,
                "sgst": sgst,
                "service_tax": service_tax
            },
            "confirm_event_data": confirm_event_details,
            "bill_details": bill_response["bill"],
            "event_price_details": bill_response["bill_details"],
            "message": "Your Booking Successfully confirmed."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
