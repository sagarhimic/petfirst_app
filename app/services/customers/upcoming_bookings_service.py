from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import date
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails


def upcoming_bookings_service(
    db: Session,
    user_id: int
):
    today = date.today()

    # -----------------------------
    # Main query (Laravel join equivalent)
    # -----------------------------
    results = (
        db.query(
            Bookings,
            BookingDetails.booking_from,
            BookingDetails.booking_time,
            case(
                (Bookings.booking_status.in_([1, 2]), "Upcoming"),
                else_=None
            ).label("status_name")
        )
        .join(
            BookingDetails,
            BookingDetails.booking_id == Bookings.booking_id
        )
        .filter(Bookings.customer_id == user_id)
        .filter(Bookings.booking_status.in_([1, 2]))
        .filter(func.date(BookingDetails.booking_from) >= today)
        .distinct()
        .order_by(Bookings.booking_date.desc())
        .all()
    )

    bookinglist = []

    for booking, booking_from, booking_time, status_name in results:

        # -----------------------------
        # Trainer service (service_type = 2)
        # -----------------------------
        if booking.service_type == 2:
            services = (
                booking.booking_detail.service.service_name
                if booking.booking_detail and booking.booking_detail.service
                else None
            )

            bookinglist.append({
                "booking_id": booking.booking_id,
                "booking_type": (
                    "Tele Medicine" if booking.booking_type == 1
                    else "House Call" if booking.booking_type == 2
                    else ""
                ),
                "service_type": booking.service_type,
                "service_name": booking.servicetype.service_name if booking.servicetype else None,
                "name": booking.trainer.name if booking.trainer else None,
                "desc": services,
                "booking_date": booking_from.strftime("%A %d %B %Y") if booking_from else None,
                "booking_time": booking_time.strftime("%I:%M %p") if booking_time else None
            })

        # -----------------------------
        # Event service (service_type = 7)
        # -----------------------------
        elif booking.service_type == 7 and booking.booking_detail and booking.booking_detail.eventname:
            ev = booking.booking_detail.eventname

            event_from = ev.event_time_from.strftime("%I:%M %p") if ev.event_time_from else ""
            event_to = ev.event_time_to.strftime("%I:%M %p") if ev.event_time_to else ""
            event_time = f"{event_from} - {event_to}"

            bookinglist.append({
                "booking_id": booking.booking_id,
                "service_type": booking.service_type,
                "service_name": booking.servicetype.service_name if booking.servicetype else None,
                "name": ev.name,
                "booking_date": ev.event_date.strftime("%A %d %B %Y") if ev.event_date else None,
                "desc": ev.location,
                "booking_time": event_time
            })

        # -----------------------------
        # Doctor service (service_type = 5)
        # -----------------------------
        elif booking.service_type == 5:
            services = (
                booking.doctor_detail.specialization
                if booking.doctor_detail else None
            )

            bookinglist.append({
                "booking_id": booking.booking_id,
                "service_type": booking.service_type,
                "service_name": booking.servicetype.service_name if booking.servicetype else None,
                "name": booking.doctor.full_name if booking.doctor else None,
                "desc": services,
                "booking_date": booking_from.strftime("%A %d %B %Y") if booking_from else None,
                "booking_time": booking_time.strftime("%I:%M %p") if booking_time else None
            })

        # -----------------------------
        # Franchise service (service_type = 3)
        # -----------------------------
        elif booking.service_type == 3:
            services = (
                booking.booking_detail.service.service_name
                if booking.booking_detail and booking.booking_detail.service
                else None
            )

            bookinglist.append({
                "booking_id": booking.booking_id,
                "service_type": booking.service_type,
                "service_name": booking.servicetype.service_name if booking.servicetype else None,
                "name": booking.franchise.location if booking.franchise else None,
                "desc": services,
                "booking_date": booking_from.strftime("%A %d %B %Y") if booking_from else None,
                "booking_time": booking_time.strftime("%I:%M %p") if booking_time else None
            })

    return {
        "status": True,
        "data": bookinglist,
        "message": "Upcoming Bookings Info."
    }
