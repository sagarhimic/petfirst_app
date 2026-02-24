
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.bookings import Bookings
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from app.models.SMS.sms_template import SMSTemplate
from app.services.SMS.sms_service import SMSHorizonService


def send_clinic_booking_notification(
    db: Session,
    booking_id: int,
    user_type: str,       # "doctor" or "customer"
    booking_type: int     # 1 = Tele Medicine, 2 = House Call
):

    booking = db.query(Bookings).filter(
        Bookings.booking_id == booking_id
    ).first()

    if not booking:
        return {"error": "Booking not found"}

    # -----------------------------
    # Booking Type Mapping
    # -----------------------------
    if booking_type == 1:
        type_name = "Tele Medicine"
    elif booking_type == 2:
        type_name = "House Call"
    else:
        type_name = ""

    # ===================================================
    # DOCTOR NOTIFICATION
    # ===================================================
    if user_type == "doctor":

        doctor = booking.doctor
        mobile = doctor.mobile
        name = doctor.full_name
        template_id = 12
        purpose = "PET Doctor Confirmation for Booking"
        link = f"franchises/get-booking-details/{booking_id}"

        title = (
            f"Dear {name}, Customer booked {type_name} appointment "
            f"- {booking_id}"
        )

        # Create Notification
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

        # NotificationUser
        noti_user = NotificationUser(
            noti_id=notification.id,
            franchise_user_id=booking.doctor_id
        )

        db.add(noti_user)
        db.commit()

    # ===================================================
    # CUSTOMER NOTIFICATION
    # ===================================================
    elif user_type == "customer":

        customer = booking.customer
        mobile = customer.mobile
        name = customer.name
        template_id = 6
        purpose = "PET Customer Doctor Booking Confirmed"
        link = f"customer/get-booking-details/{booking_id}"

        title = (
            f"Dear {name}, you confirmed Clinic Appointment "
            f"- {booking_id}"
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
    # COMMON SMS SECTION
    # ===================================================

    sms_template = db.query(SMSTemplate).filter(
        SMSTemplate.id == template_id
    ).first()

    if sms_template:

        text = sms_template.content

        text = text.replace("{doctor}", booking.doctor.full_name if booking.doctor else "")
        text = text.replace("{customer}", booking.customer.name if booking.customer else "")
        text = text.replace("{booking_type}", type_name)
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