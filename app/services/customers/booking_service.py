from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.utils.helpers import format_date, format_date_db

PER_PAGE = 10


def get_customer_bookings(
    db: Session,
    user_id: int,
    search_key: str | None,
    status_id: list[int] | None,
    booking_from: str | None,
    booking_to: str | None,
    booking_type: int | None,
    page: int
):
    # -------------------------------------------------
    # Base query
    # -------------------------------------------------
    query = (
        db.query(Bookings)
        .filter(Bookings.customer_id == user_id)
        .options(
            joinedload(Bookings.booking_detail)
                .joinedload(BookingDetails.eventname),
            joinedload(Bookings.trainer),
            joinedload(Bookings.doctor),
            joinedload(Bookings.franchise),
            joinedload(Bookings.servicetype),
            joinedload(Bookings.bookingstatus),
        )
    )

    # -------------------------------------------------
    # Booking type
    # -------------------------------------------------
    if booking_type:
        query = query.filter(Bookings.service_type == booking_type)

    # -------------------------------------------------
    # Search key
    # -------------------------------------------------
    if search_key:
        query = query.filter(
            or_(
                Bookings.booking_id == search_key,
                Bookings.trainer.has(
                    Bookings.trainer.property.mapper.class_.name.ilike(f"%{search_key}%")
                ),
                Bookings.doctor.has(
                    Bookings.doctor.property.mapper.class_.full_name.ilike(f"%{search_key}%")
                ),
            )
        )

    # -------------------------------------------------
    # Date filters
    # -------------------------------------------------
    if booking_from and booking_to:
        query = query.filter(
            func.date(Bookings.booking_date).between(
                format_date_db(booking_from),
                format_date_db(booking_to)
            )
        )
    elif booking_from:
        query = query.filter(
            func.date(Bookings.booking_date) >= format_date_db(booking_from)
        )

    # -------------------------------------------------
    # Status filter
    # -------------------------------------------------
    if status_id:
        status_id = [s for s in status_id if s]
        if status_id:
            query = query.filter(Bookings.booking_status.in_(status_id))

    # -------------------------------------------------
    # Pagination
    # -------------------------------------------------
    total = query.count()

    results = (
        query
        .order_by(Bookings.created_at.desc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
        .all()
    )

    bookings = []

    # -------------------------------------------------
    # Result formatting (Laravel foreach equivalent)
    # -------------------------------------------------
    for r in results:

        # FIRST booking detail (Laravel: $result->bookingDetail->first())
        bd = r.booking_detail
        ev = bd.eventname if bd and bd.eventname else None

        # -----------------------------
        # Name based on service_type
        # -----------------------------
        name = ""

        if r.service_type == 7:  # Event
            name = ev.name if ev else None
        elif r.service_type == 2:  # Trainer
            name = r.trainer.name if r.trainer else None
        elif r.service_type == 5:  # Doctor
            name = r.doctor.full_name if r.doctor else None
        elif r.service_type == 3:  # Franchise
            name = f"Pet-first-{r.franchise.location}" if r.franchise else None

        # -----------------------------
        # Event time
        # -----------------------------
        event_time = ""
        if ev and ev.event_time_from and ev.event_time_to:
            event_time = (
                f"{ev.event_time_from.strftime('%I:%M %p')} - "
                f"{ev.event_time_to.strftime('%I:%M %p')}"
            )

        bookings.append({
            "booking_id": r.booking_id,

            # Laravel: $result->bookingDetail()->count()
            "service_count": 1 if r.booking_detail else 0,

            "booking_date": format_date(r.booking_date) if r.booking_date else None,

            "event_date": (
                format_date(ev.event_date)
                if ev and ev.event_date else None
            ),

            "event_time": event_time,

            "franchise": (
                f"Pet-first-{r.franchise.location}"
                if r.franchise else None
            ),

            "service_name": (
                r.servicetype.service_name
                if r.servicetype else None
            ),

            "trainer_name": name,

            "total_amount": r.total_amount,
            "discount": r.discount,

            "booking_type": (
                "Tele Medicine"
                if r.booking_type == 1
                else "House Call"
                if r.booking_type == 2
                else ""
            ),

            "booking_status": (
                r.bookingstatus.name
                if r.bookingstatus else None
            ),

            "status_color_code": (
                r.bookingstatus.color_code
                if r.bookingstatus else None
            ),

            "booking_created": (
                format_date(r.created_at)
                if r.created_at else None
            )
        })

    last_page = (total + PER_PAGE - 1) // PER_PAGE

    return {
        "status": True,
        "data": bookings,
        "message": "Bookings Info.",
        "total": total,
        "per_page": PER_PAGE,
        "current_page": page,
        "last_page": last_page,
        "from": ((page - 1) * PER_PAGE) + 1 if total else None,
        "to": min(page * PER_PAGE, total),
        "has_more_pages": page < last_page
    }
