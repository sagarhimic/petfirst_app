# app/services/customers/doctor_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from math import radians
from app.models.Franchises.doctor_info import DoctorInfo
from app.models.Franchises.doctor import Doctor
from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_review import FranchiseReview
from app.models.Franchises.doctor_review import DoctorReview
from app.models.bookings import Bookings
from app.models.user_location import UserLocation

EARTH_RADIUS = 6371
PER_PAGE = 10


def get_doctors_service(
    db: Session,
    request,
    user_id: int,
    franchise_id: int,
    latitude: float | None,
    longitude: float | None,
    search_key: str | None,
    page: int,
):
    # -----------------------------
    # Get user location fallback
    # -----------------------------
    if not latitude or not longitude:
        location = (
            db.query(UserLocation)
            .filter(UserLocation.user_id == user_id)
            .filter(UserLocation.is_primary == 1)
            .first()
        )
        latitude = location.latitude
        longitude = location.longitude

    lat = radians(latitude)
    lng = radians(longitude)

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
    # Nearby doctor query
    # -----------------------------
    query = (
        db.query(
            Doctor.id,
            Doctor.full_name.label("doctor_name"),
            Franchise.id.label("franchise_id"),
            Franchise.location,
            Franchise.city,
            Franchise.image,
            Franchise.contact_number,
            Doctor.mobile,
            Doctor.status,
            Doctor.profile_pic,
            DoctorInfo.specialization,
            DoctorInfo.exp,
            DoctorInfo.availability,
            DoctorInfo.consultation_fee,
            distance,
        )
        .join(DoctorInfo, DoctorInfo.doctor_id == Doctor.id)
        .join(Franchise, DoctorInfo.franchise_id == Franchise.id)
        .filter(Franchise.status_id == 1)
        .filter(Franchise.id == franchise_id)
    )

    if search_key:
        query = query.filter(User.full_name.ilike(f"%{search_key}%"))

    query = query.order_by(distance)

    total = query.count()
    rows = query.offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()

    # -----------------------------
    # Response building
    # -----------------------------
    response = {"franchise": None, "doctors": []}

    for d in rows:
        # Franchise reviews
        reviews = (
            db.query(FranchiseReview.rating)
            .filter(FranchiseReview.franchise_id == d.franchise_id)
            .all()
        )
        ratings = [r.rating for r in reviews]
        avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

        booking_count = (
            db.query(Bookings)
            .filter(Bookings.franchise_id == d.franchise_id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        # Franchise info (once)
        if response["franchise"] is None:
            response["franchise"] = {
                "franchise_id": d.franchise_id,
                "franchise_name": "Pet-first",
                "location": d.location,
                "image": f"{request.base_url}{d.image.lstrip('/')}" if d.image else None,
                "mobile": "9577791111",
                "distance": f"{round(d.distance, 2)}(kms)",
                "serviceble": True,
                "rating": int(avg_rating),
                "total_reviews": len(ratings),
                "total_franchise_bookings": booking_count,
            }

        # Skip empty doctor rows
        if not any(
            [d.doctor_name, d.mobile, d.profile_pic, d.specialization, d.exp]
        ):
            continue

        # Doctor reviews
        doc_reviews = (
            db.query(DoctorReview.rating)
            .filter(DoctorReview.doctor_id == d.id)
            .all()
        )
        doc_ratings = [r.rating for r in doc_reviews]
        avg_doc_rating = (
            round(sum(doc_ratings) / len(doc_ratings), 2) if doc_ratings else 0
        )

        doc_booking_count = (
            db.query(Bookings)
            .filter(Bookings.doctor_id == d.id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        response["doctors"].append(
            {
                "doctor_id": d.id,
                "name": d.doctor_name,
                "mobile": d.mobile,
                "profile_pic": f"{request.base_url}{d.profile_pic.lstrip('/')}"
                if d.profile_pic
                else None,
                "exp": d.exp or 0,
                "fee": d.consultation_fee or 0,
                "tele_medicine": None,
                "house_call": None,
                "distance": f"{round(d.distance, 2)}(kms)",
                "doctor_rating": int(avg_doc_rating),
                "total_doctor_reviews": len(doc_ratings),
                "total_patients": doc_booking_count,
                "status": "Available" if d.status == 1 else "Not Available",
            }
        )

    last_page = (total + PER_PAGE - 1) // PER_PAGE

    return {
        "status": True,
        "data": response,
        "message": "Doctors Info.",
        "total": total,
        "per_page": PER_PAGE,
        "current_page": page,
        "last_page": last_page,
        "from": (page - 1) * PER_PAGE + 1 if total else 0,
        "to": min(page * PER_PAGE, total),
        "has_more_pages": page < last_page,
    }
