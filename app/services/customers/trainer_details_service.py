from fastapi import Request, HTTPException
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.trainer_personal_info import TrainerPersonalInfo
from app.models.trainer_review import TrainerReview
from app.models.bookings import Bookings
from app.models.sub_services import SubService
from app.models.service_images import ServiceImages
from app.models.booking_details import BookingDetails
from app.models.trainers.trainer_service_reviews import TrainerServiceReview
from app.models.sub_category_services import SubCategoryServices
from app.models.user_location import UserLocation
from app.models.trainers.assign_trainer_service import UserService
from app.utils.helpers import format_time, rating_perc
from app.services.customers.trainer_service import get_nearby_trainer_locations
from sqlalchemy import select
from app.core.config import settings


def trainer_details_service(db: Session, trainer_id: int, data):
    
    try:
        latitude = data.latitude
        longitude = data.longitude

        # -----------------------------
        # Trainer basic data
        # -----------------------------
        trainer_services = (
            db.query(UserService)
            .filter(UserService.trainer_id == trainer_id)
            .all()
        )

        trainer_reviews = (
            db.query(TrainerReview)
            .filter(TrainerReview.trainer_id == trainer_id)
            .all()
        )

        trainer_info = (
            db.query(TrainerPersonalInfo)
            .filter(TrainerPersonalInfo.trainer_id == trainer_id)
            .first()
        )

        total_reviews_count = len(trainer_reviews)
        current_date = date.today()

        # -----------------------------
        # Booked Dates
        # -----------------------------
        booked_ids = (
            select(Bookings.booking_id)
            .where(Bookings.trainer_id == trainer_id)
            .where(Bookings.booking_status.in_([1, 2]))
        )

        booked_dates_rows = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_from >= current_date)
            .filter(BookingDetails.booking_id.in_(booked_ids))
            .all()
        )

        booked_dates = [
            {
                "date": row.booking_from.strftime("%Y-%m-%d"),
                "time": format_time(row.booking_time),
            }
            for row in booked_dates_rows
        ]

        # -----------------------------
        # Trainer Rating Breakdown
        # -----------------------------
        rating_info = (
            db.query(
                TrainerReview.rating,
                func.count().label("count")   # ✅ FIXED
            )
            .filter(TrainerReview.trainer_id == trainer_id)
            .group_by(TrainerReview.rating)
            .all()
        )

        rating_counts = {i: 0 for i in range(1, 6)}
        for r in rating_info:
            rating_counts[r.rating] = r.count

        rating = [
            {
                "rating": k,
                "count": v,
                "rating_perc": rating_perc(v, total_reviews_count)
            }
            for k, v in rating_counts.items()
        ]

        # -----------------------------
        # Services + Service Reviews
        # -----------------------------
        services = []

        for srv in trainer_services:
            service_reviews = (
                db.query(TrainerServiceReview)
                .filter(TrainerServiceReview.trainer_id == trainer_id)
                .filter(TrainerServiceReview.service_id == srv.service_id)
                .all()
            )

            service_booking_count = (
                db.query(BookingDetails)
                .filter(BookingDetails.service_id == srv.service_id)
                .count()
            )

            service_includes = (
                db.query(SubCategoryServices)
                .filter(SubCategoryServices.sub_service_id == srv.service_id)
                .all()
            )

            includes = [{"service_name": row.category.service_name} for row in service_includes]

            total_ser_reviews = len(service_reviews)
            avg_ser_rating = (
                round(sum(r.rating for r in service_reviews) / total_ser_reviews, 2)
                if total_ser_reviews else 0
            )

            ser_reviews = [
                {
                    "rating": r.rating,
                    "review": r.review_text,
                    "total_review_users": total_ser_reviews
                }
                for r in service_reviews
            ]

            service_images = get_service_images(
                db=db,
                service_id=srv.service_id,
                franchise_id=None
            )

            services.append({
                "overal_rating": int(avg_ser_rating),
                "service_id": srv.subservice.id,
                "total_service_bookings": service_booking_count,
                "total_review_users": total_ser_reviews,
                "service_image": service_images,  # hook if needed
                "duration": srv.subservice.duration,
                "service_name": srv.subservice.service_name,
                "description": srv.subservice.description,
                "price": srv.price,
                "service_includes": includes,
                "service_reviews": ser_reviews,
            })

        # -----------------------------
        # Trainer Reviews
        # -----------------------------
        reviews = []
        avg_rating = (
            round(sum(r.rating for r in trainer_reviews) / total_reviews_count, 2)
            if total_reviews_count else 0
        )

        for r in trainer_reviews:
            location = (
                db.query(UserLocation)
                .filter(UserLocation.user_id == r.customer_id)
                .filter(UserLocation.is_primary == 1)
                .first()
            )

            reviews.append({
                "customer": r.customer.name,
                "location": location.city if location else None,
                "profile_pic": r.userinfo.profile_pic if r.userinfo else None,
                "service": r.service.service_name if r.service else None,
                "rating": r.rating,
                "review": r.review_text,
            })

        # -----------------------------
        # Distance
        # -----------------------------
        nearby = get_nearby_trainer_locations(
            db, latitude, longitude, 150, None, trainer_id
        )

        first = nearby[0] if nearby else None

        trainer_personal_info = {
            "trainer_id": first.id if first else None,
            "name": first.trainer_name if first else None,
            "mobile": first.mobile if first else None,
            "profile_pic": first.profile_pic if first else None,
            "location": first.location if first else None,
            "exp": first.exp if first else 0,
            "distance": f"{round(first.distance, 2)}(kms)" if first else ""
        }

        trainer_booking_count = (
            db.query(Bookings)
            .filter(Bookings.trainer_id == trainer_id)
            .count()
        )

        return {
            "status": True,
            "service_type": 2,
            "data": trainer_personal_info,
            "trainer_ratings": rating,
            "trainer_overal_rating": int(avg_rating),
            # "trainer_total_bookings": len(booked_ids),
            "trainer_total_bookings": trainer_booking_count,  # ✅ FIXED
            "trainer_exp": trainer_info.exp if trainer_info else "",
            "services": services,
            "about": trainer_info.about if trainer_info else "",
            "reviews": reviews,
            "booked_dates": booked_dates,
            "exist_cart_services": [],
            "message": "Trainer Details Info."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def get_service_images(
    db: Session,
    service_id: int,
    franchise_id: int | None = None
):
    # -----------------------------
    # Get package_type
    # -----------------------------
    package_type = (
        db.query(SubService.package_type)
        .filter(SubService.id == service_id)
        .scalar()
    )

    # -----------------------------
    # Base query (NO limit yet)
    # -----------------------------
    query = (
        db.query(ServiceImages)
        .filter(ServiceImages.service_id == service_id)
        .order_by(ServiceImages.created_at.desc())
    )

    # -----------------------------
    # Apply franchise logic
    # -----------------------------
    if package_type == 1:
        query = query.filter(
            (ServiceImages.franchise_id == franchise_id) |
            (ServiceImages.franchise_id.is_(None))
        )

    elif package_type == 2:
        query = query.filter(ServiceImages.franchise_id.is_(None))

    # -----------------------------
    # Apply LIMIT LAST ✅
    # -----------------------------
    results = query.limit(6).all()

    if not results:
        return []

    # -----------------------------
    # Format response safely
    # -----------------------------

    return [
    {
        "image": f"{settings.BASE_URL}/{row.image.lstrip('/')}"
        if row.image else None
    }
    for row in results
]
