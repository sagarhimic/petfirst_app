from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_review import FranchiseReview
from app.models.bookings import Bookings
from math import radians
from app.utils.helpers import build_full_url

RECORDS_PER_PAGE = 10
EARTH_RADIUS = 6371  # KM


def get_franchises_service(
    db: Session,
    request: Request,
    latitude: float,
    longitude: float,
    page: int,
    search_key: str | None
):
    radius = 150

    lat = radians(latitude)
    lng = radians(longitude)

    # -----------------------------
    # Distance calculation
    # -----------------------------
    distance = (
        EARTH_RADIUS
        * func.acos(
            func.cos(lat)
            * func.cos(func.radians(Franchise.latitude))
            * func.cos(func.radians(Franchise.longitude) - lng)
            + func.sin(lat)
            * func.sin(func.radians(Franchise.latitude))
        )
    ).label("distance")

    # -----------------------------
    # Base query
    # -----------------------------
    query = (
        db.query(
            Franchise.id.label("franchise_id"),
            Franchise.location,
            Franchise.city,
            Franchise.state,
            Franchise.contact_number,
            Franchise.image,
            distance
        )
        .filter(Franchise.status_id == 1)
    )

    if search_key:
        query = query.filter(Franchise.city.ilike(f"%{search_key}%"))

    # -----------------------------
    # Distance filter
    # -----------------------------
    query = query.filter(distance <= radius).order_by(distance)

    # -----------------------------
    # Pagination
    # -----------------------------
    total = query.count()
    offset = (page - 1) * RECORDS_PER_PAGE
    rows = query.offset(offset).limit(RECORDS_PER_PAGE).all()

    # -----------------------------
    # Build response
    # -----------------------------
    franchises = []

    for f in rows:
        reviews = (
            db.query(FranchiseReview.rating)
            .filter(FranchiseReview.franchise_id == f.franchise_id)
            .all()
        )

        ratings = [r.rating for r in reviews]
        total_reviews = len(ratings)
        avg_rating = round(sum(ratings) / total_reviews, 2) if total_reviews else 0

        booking_count = (
            db.query(Bookings)
            .filter(Bookings.franchise_id == f.franchise_id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        franchises.append({
            "franchise_id": f.franchise_id,
            "franchise_name": "Pet-first",
            "location": f.location,
            "city": f.city,
            "state": f.state,
            "mobile": f.contact_number,
            "image": build_full_url(request, f.image),
            "distance": f"{round(f.distance, 2)} (kms)",
            "rating": int(avg_rating),
            "total_reviews": total_reviews,
            "total_franchise_bookings": booking_count
        })

    # -----------------------------
    # Laravel-style pagination meta
    # -----------------------------
    last_page = (total + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

    return {
        "status": True,
        "data": franchises,
        "message": "Franchises Info.",
        "total": total,
        "per_page": RECORDS_PER_PAGE,
        "current_page": page,
        "last_page": last_page,
        "from": offset + 1 if total else 0,
        "to": min(offset + RECORDS_PER_PAGE, total),
        "has_more_pages": page < last_page
    }
