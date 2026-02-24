
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.bookings import Bookings
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from app.models.SMS.sms_template import SMSTemplate
from app.services.SMS.sms_service import SMSHorizonService


def send_reschedule_grooming_booking_notification(
    db: Session,
    booking_id: int,
    user_type: str  # "franchise" or "customer"
):

    booking = db.query(Bookings).filter(
        Bookings.booking_id == booking_id
    ).first()

    if not booking:
        return {"error": "Booking not found"}

    # ===================================================
    # FRANCHISE NOTIFICATION
    # ===================================================
    if user_type == "franchise":

        mobile = "8106176863"
        name = "Pet-First"
        template_id = 14
        purpose = "PET First Grooming Reschedule Booking"
        link = f"franchise/get-booking-details/{booking_id}"

        title = (
            f"Customer Reschedule booking Grooming Service. "
            f"Booking ID - {booking_id}"
        )

        notification = Notification(
            type_id=booking.service_type,
            title=title,
            link=link,
            booking_id=booking_id,
            created_at=datetime.utcnow()
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        noti_user = NotificationUser(
            noti_id=notification.id,
            franchise_id=booking.franchise_id
        )

        db.add(noti_user)
        db.commit()

    # ===================================================
    # CUSTOMER NOTIFICATION
    # ===================================================
    elif user_type == "customer":

        mobile = booking.customer.mobile
        name = booking.customer.name
        template_id = 9
        purpose = "PET Customer Reschedule Grooming Booking"
        link = f"customer/get-booking-details/{booking_id}"

        title = (
            f"Dear {name}, you confirmed Reschedule Grooming Service "
            f"Booking ID - {booking_id}"
        )

        notification = Notification(
            type_id=booking.service_type,
            title=title,
            link=link,
            booking_id=booking_id,
            created_at=datetime.utcnow()
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        noti_user = NotificationUser(
            noti_id=notification.id,
            customer_id=booking.customer_id
        )

        db.add(noti_user)
        db.commit()

    else:
        return {"error": "Invalid user type"}

    # ===================================================
    # OPTIONAL SMS SECTION (Uncomment if Needed)
    # ===================================================

    sms_template = db.query(SMSTemplate).filter(
        SMSTemplate.id == template_id
    ).first()

    if sms_template and mobile:

        text = sms_template.content
        text = text.replace("{customer}", booking.customer.name if booking.customer else "")
        text = text.replace("{booking_id}", str(booking_id))

        SMSHorizonService.send_sms(
            db=db,
            params={
                "mobile": mobile,
                "message": text,
                "purpose": purpose,
                "sms_template_id": template_id,
                "receiver_name": name
            }
        )

    return {"status": True}