from sqlalchemy.orm import Session
from datetime import datetime

from app.models.Franchises.Events.events import Event
from app.models.Franchises.Events.event_gallery import EventGallery
from app.models.Franchises.Events.event_benefits import EventBenefit
from app.utils.helpers import build_full_url, format_date

PER_PAGE = 10


def get_events_list_service(
    db: Session,
    request,
    user_id: int,
    page: int,
    search_key: str | None
):
    # --------------------------------
    # Base query
    # --------------------------------
    query = (
        db.query(Event)
        .filter(Event.status_id == 1)
        .filter(Event.event_date >= datetime.utcnow())
    )

    if search_key:
        query = query.filter(Event.name.ilike(f"%{search_key}%"))

    # --------------------------------
    # Pagination
    # --------------------------------
    total = query.count()

    results = (
        query
        .order_by(Event.event_date.asc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
        .all()
    )

    event_lists = []

    for event in results:
        gallery = (
            db.query(EventGallery)
            .filter(EventGallery.event_id == event.id)
            .all()
        )

        benefits = (
            db.query(EventBenefit)
            .filter(EventBenefit.event_id == event.id)
            .all()
        )

        event_lists.append({
            "event_id": event.id,
            "event_name": event.name,
            "event_type": "Event" if event.type == 1 else "Activity",
            "about": event.about,
            "event_date": format_date(event.event_date),
            "event_time_from": event.event_time_from,
            "event_time_to": event.event_time_to,
            "location": event.location,
            "city": event.city,
            "state_id": event.state_id,
            "state": event.state.name if event.state else None,
            "country_id": event.country_id,
            "country": event.country.name if event.country else None,
            "pincode": event.pincode,
            "entry_fee": event.entry_fee,
            "status_id": event.status_id,
            "gallery": [
                {"image": build_full_url(request, g.image)}
                for g in gallery
            ] if gallery else None,
            "benefits": [
                {"benefit": b.benefit}
                for b in benefits
            ] if benefits else None
        })

    last_page = (total + PER_PAGE - 1) // PER_PAGE

    return {
        "status": True,
        "data": event_lists,
        "message": "Events Info.",
        "total": total,
        "per_page": PER_PAGE,
        "current_page": page,
        "last_page": last_page,
        "from": (page - 1) * PER_PAGE + 1 if total else None,
        "to": min(page * PER_PAGE, total) if total else None,
        "has_more_pages": page < last_page
    }
