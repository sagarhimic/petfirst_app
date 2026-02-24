from sqlalchemy.orm import Session
from sqlalchemy import func
from math import radians
from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_service import FranchiseService
from app.models.Franchises.franchise_review import FranchiseReview
from app.models.bookings import Bookings
from app.models.user_location import UserLocation

PER_PAGE = 10
EARTH_RADIUS = 6371  # km


def get_grooming_service(
    db: Session,
    request,
    user_id: int,
    latitude: float | None,
    longitude: float | None,
    page: int,
    search_key: str | None
):
    # -----------------------------
    # Get user primary location
    # -----------------------------
    location_data = (
        db.query(UserLocation)
        .filter(UserLocation.user_id == user_id)
        .filter(UserLocation.is_primary == 1)
        .first()
    )

    if not location_data:
        return {
            "status": False,
            "message": "User location not found."
        }

    latitude = latitude if latitude else location_data.latitude
    longitude = longitude if longitude else location_data.longitude

    radius = 150

    nearby_locations, pagination = get_nearby_grooming_locations(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        page=page,
        search_key=search_key
    )

    franchises = []

    for franchise in nearby_locations:

        # -----------------------------
        # Reviews
        # -----------------------------
        ratings = (
            db.query(FranchiseReview.rating)
            .filter(FranchiseReview.franchise_id == Franchise.id)
            .all()
        )

        total_reviews = len(ratings)
        avg_rating = (
            round(sum(r.rating for r in ratings) / total_reviews, 2)
            if total_reviews > 0 else 0
        )

        # -----------------------------
        # Booking count
        # -----------------------------
        booking_counts = (
            db.query(Bookings)
            .filter(Bookings.franchise_id == Franchise.id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        franchises.append({
            "franchise_name": "Pet-first",
            "franchise_id": franchise.id,
            "location": franchise.location,
            "city": franchise.city,
            "state": franchise.state,
            "mobile": franchise.contact_number,
            "distance": f"{round(franchise.distance,2)}(kms)",
            "rating": int(avg_rating),
            "total_reviews": total_reviews,
            "total_bookings": booking_counts,
            "status": "Available" if franchise.status_id == 1 else "Not Available"
        })

    return {
        "status": True,
        "data": franchises,
        "message": "Franchises Info.",
        **pagination
    }

def get_nearby_grooming_locations(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    page: int,
    search_key: str | None
):
    lat = radians(latitude)
    lng = radians(longitude)

    distance = (
        EARTH_RADIUS * func.acos(
            func.cos(lat)
            * func.cos(func.radians(Franchise.latitude))
            * func.cos(func.radians(Franchise.longitude) - lng)
            + func.sin(lat)
            * func.sin(func.radians(Franchise.latitude))
        )
    ).label("distance")

    # -----------------------------
    # Subquery (calculate distance)
    # -----------------------------
    subquery = (
    db.query(
        Franchise.id.label("id"),
        Franchise.location,
        Franchise.city,
        Franchise.state,
        Franchise.contact_number,
        Franchise.status_id,
        distance
    )
    .join(
        FranchiseService,
        FranchiseService.franchise_id == Franchise.id
    )
    .filter(Franchise.status_id == 1)
    .filter(FranchiseService.service_type == 3)
    .group_by(
        Franchise.id,
        Franchise.location,
        Franchise.city,
        Franchise.state,
        Franchise.contact_number,
        Franchise.status_id
    )
)

    if search_key:
        subquery = subquery.filter(
            Franchise.city.ilike(f"%{search_key}%")
        )

    subquery = subquery.subquery()

    # -----------------------------
    # Outer query (filter by distance)
    # -----------------------------
    query = (
        db.query(subquery)
        .filter(subquery.c.distance <= radius)
        .order_by(subquery.c.distance.asc())
    )

    total = query.count()

    results = (
        query.offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
        .all()
    )

    pagination = {
        "total": total,
        "per_page": PER_PAGE,
        "current_page": page,
        "last_page": (total // PER_PAGE) + (1 if total % PER_PAGE else 0),
        "from": (page - 1) * PER_PAGE + 1 if total > 0 else 0,
        "to": min(page * PER_PAGE, total),
        "has_more_pages": page * PER_PAGE < total
    }

    return results, pagination

