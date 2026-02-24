# app/services/customers/doctor_details_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from math import radians

from app.models.Franchises.doctor_review import DoctorReview
from app.models.Franchises.doctor_info import DoctorInfo
from app.models.Franchises.doctor_gallery import DoctorGallery
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.user_location import UserLocation

from app.utils.common import rating_perc, format_time
from app.services.customers.doctor_nearby_service import get_nearby_doctor
from fastapi import HTTPException, Request

EARTH_RADIUS = 6371


def doctor_details_service(
    db: Session,
    request,
    user_id: int,
    doctor_id: int
):
    try:
        # -----------------------------
        # Doctor Reviews
        # -----------------------------
        doctor_reviews = (
            db.query(DoctorReview)
            .filter(DoctorReview.doctor_id == doctor_id)
            .all()
        )

        total_reviews = len(doctor_reviews)

        # Rating distribution
        rating_groups = (
            db.query(
                DoctorReview.rating,
                func.count(DoctorReview.rating).label("count")
            )
            .filter(DoctorReview.doctor_id == doctor_id)
            .group_by(DoctorReview.rating)
            .all()
        )

        rating_map = {i: 0 for i in range(1, 6)}
        for r in rating_groups:
            rating_map[r.rating] = r.count

        ratings = []
        for rating_value, count in rating_map.items():
            ratings.append({
                "rating": rating_value,
                "count": count,
                "rating_perc": rating_perc(count, total_reviews)
            })

        # Average rating
        avg_rating = (
            round(sum(r.rating for r in doctor_reviews) / total_reviews, 2)
            if total_reviews > 0 else 0
        )

        # -----------------------------
        # Review list
        # -----------------------------
        reviews = []
        for review in doctor_reviews:
            location = (
                db.query(UserLocation)
                .filter(UserLocation.user_id == review.customer_id)
                .filter(UserLocation.is_primary == 1)
                .first()
            )

            reviews.append({
                "customer": review.customer.name if review.customer else "",
                "location": location.city if location else None,
                "profile_pic": review.user.profile_pic if review.user else None,
                "service": review.service.service_name if review.service else None,
                "rating": review.rating,
                "review": review.review_text
            })

        # -----------------------------
        # User Location (for distance)
        # -----------------------------
        user_location = (
            db.query(UserLocation)
            .filter(UserLocation.user_id == user_id)
            .filter(UserLocation.is_primary == 1)
            .first()
        )

        if not user_location:
            raise HTTPException(status_code=400, detail="User location not found")

        # -----------------------------
        # Nearby Doctor (distance)
        # -----------------------------
        nearby = get_nearby_doctor(
            db=db,
            latitude=user_location.latitude,
            longitude=user_location.longitude,
            doctor_id=doctor_id
        )

        if not nearby:
            raise HTTPException(status_code=404, detail="Doctor not found")

        doctor = nearby[0]

        # Charges (mock same as Laravel)
        telemedicine_charge = None
        house_call_charge = None

        doctor_booking_count = (
            db.query(Bookings)
            .filter(Bookings.doctor_id == doctor_id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        doctor_personal_info = {
            "doctor_id": doctor.id,
            "name": doctor.doctor_name,
            "mobile": "9577791111",
            "profile_pic": f"{request.base_url}{doctor.profile_pic.lstrip('/')}" if doctor.profile_pic else None,
            "location": doctor.location,
            "exp": doctor.exp or 0,
            "fee": doctor.consultation_fee or 0,
            "distance": f"{round(doctor.distance, 2)}(kms)",
            "tele_medicine": telemedicine_charge,
            "house_call": house_call_charge,
            "total_patients": doctor_booking_count,
            "status": "Available" if doctor.status == 1 else "Not Available"
        }

        location_info = {
            "franchise_name": "petfirst",
            "location": doctor.location,
            "city": doctor.city,
            "state": doctor.state,
            "contact_number": "9577791111",
            "pin_code": doctor.pin_code,
            "latitude": doctor.latitude,
            "longitude": doctor.longitude,
            "distance": f"{round(doctor.distance, 2)}(kms)"
        }

        # -----------------------------
        # Gallery
        # -----------------------------
        gallery = (
            db.query(DoctorGallery)
            .filter(DoctorGallery.doctor_id == doctor_id)
            .all()
        )

        gallery_info = [{"image": g.image} for g in gallery]

        # -----------------------------
        # Booked Dates
        # -----------------------------
        today = date.today()

        booked_ids = (
            db.query(Bookings.booking_id)
            .filter(Bookings.doctor_id == doctor_id)
            .filter(Bookings.booking_status.in_([1, 2]))
            .subquery()
        )

        booked_details = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_from >= today)
            .filter(BookingDetails.booking_id.in_(booked_ids))
            .all()
        )

        booked_dates = [
            {
                "date": bd.booking_from.strftime("%Y-%m-%d"),
                "time": format_time(bd.booking_time)
            }
            for bd in booked_details
        ]

        # -----------------------------
        # Final Response
        # -----------------------------
        return {
            "status": True,
            "service_type": 5,
            "data": doctor_personal_info,
            "doctor_ratings": ratings,
            "doctor_overal_rating": int(avg_rating),
            "exp": doctor.exp,
            "about": doctor.description,
            "location": location_info,
            "gallery": gallery_info,
            "reviews": reviews,
            "booked_dates": booked_dates,
            "message": "Doctor Details Info."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )
