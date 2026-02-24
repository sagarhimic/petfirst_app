
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.bookings import Bookings
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from app.models.SMS.sms_template import SMSTemplate
from app.services.SMS.sms_service import SMSHorizonService


def send_booking_notification(
    db: Session,
    booking_id: int,
    user_type: str  # "trainer" or "customer"
):

    booking = db.query(Bookings).filter(
        Bookings.booking_id == booking_id
    ).first()

    if not booking:
        return {"error": "Booking not found"}

    if user_type == "trainer":

        name = booking.trainer.name
        mobile = booking.trainer.mobile
        template_id = 3
        purpose = "PET Trainer Confirmed Booking"
        link = f"trainer/get-booking-details/{booking_id}"
        title = (
            f"Dear {name}, Customer booked Trainer Service. "
            f"Booking ID - {booking_id}"
        )

        noti_user_field = {
            "trainer_id": booking.trainer_id
        }

    elif user_type == "customer":

        name = booking.customer.name
        mobile = booking.customer.mobile
        template_id = 2
        purpose = "PET Customer Trainer Booking"
        link = f"customer/get-booking-details/{booking_id}"
        title = (
            f"Dear {name}, you confirmed Trainer Booking. "
            f"Booking ID - {booking_id}"
        )

        noti_user_field = {
            "customer_id": booking.customer_id
        }

    else:
        return {"error": "Invalid user type"}

    # ========================
    # 1️⃣ Create Notification
    # ========================

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

    # ========================
    # 2️⃣ Insert NotificationUser
    # ========================

    noti_user = NotificationUser(
        noti_id=notification.id,
        **noti_user_field
    )

    db.add(noti_user)
    db.commit()

    # ========================
    # 3️⃣ Send SMS
    # ========================

    sms_template = db.query(SMSTemplate).filter(
        SMSTemplate.id == template_id
    ).first()

    if sms_template:

        text = sms_template.content

        # Replace dynamic fields
        text = text.replace("{trainer}", booking.trainer.name)
        text = text.replace("{customer}", booking.customer.name)
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