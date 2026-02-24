from fastapi import Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from math import radians
from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_service_review import FranchiseServiceReview
from app.models.Franchises.franchise_review import FranchiseReview
from app.models.Franchises.franchise_service import FranchiseService
from app.models.service_images import ServiceImages
from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.user_location import UserLocation
from app.models.sub_services import SubService
from app.models.sub_category_services import SubCategoryServices
from sqlalchemy import or_
from datetime import datetime
from app.utils.helpers import build_full_url
from app.utils.common import checkDistanceRange
from app.services.customers.grooming.get_nearby_grooming_service import get_nearby_grooming


def grooming_details_service(
    db: Session,
    franchise_id: int,
    user_id: int,
    package_type: int | None,
    search_key: str | None,
    request: Request
):
    try:
        # --------------------------------------------------
        # Franchise Reviews
        # --------------------------------------------------
        franchise_reviews = (
            db.query(FranchiseReview)
            .filter(FranchiseReview.franchise_id == franchise_id)
            .all()
        )

        total_reviews = len(franchise_reviews)
        booking_counts = (
            db.query(Bookings)
            .filter(
                Bookings.franchise_id == franchise_id,
                Bookings.booking_status == 4
            )
            .count()
        )

        average_rating = 0
        if total_reviews > 0:
            average_rating = round(
                sum(r.rating for r in franchise_reviews) / total_reviews,
                2
            )

        reviews = []
        for review in franchise_reviews:
            location = (
                db.query(UserLocation)
                .filter(
                    UserLocation.user_id == review.user_id,
                    UserLocation.is_primary == 1
                )
                .first()
            )

            reviews.append({
                "customer": review.customer.name if review.customer else None,
                "location": location.city if location else None,
                "profile_pic": build_file_url(
                    request,
                    review.customer.userinfo.profile_pic
                ) if review.customer and review.customer.userinfo else None,
                "rating": review.rating,
                "review": review.review_text
            })

        # --------------------------------------------------
        # Grooming Services
        # --------------------------------------------------
        grooming_query = (
            db.query(FranchiseService)
            .filter(
                FranchiseService.franchise_id == franchise_id,
                FranchiseService.service_type == 3
            )
        )

        if package_type:
            grooming_query = grooming_query.join(SubService).filter(
                SubService.package_type == package_type
            )

        if search_key:
            grooming_query = grooming_query.join(SubService).filter(
                SubService.service_name.ilike(f"%{search_key}%")
            )

        grooming_services = grooming_query.all()

        services = []
        exist_services = []

        for result in grooming_services:

            sub = result.subservice

            # Service Reviews
            service_reviews = (
                db.query(FranchiseServiceReview)
                .filter(
                    FranchiseServiceReview.service_id == result.service_id
                )
                .all()
            )

            total_ser_reviews = len(service_reviews)
            average_ser_rating = 0

            if total_ser_reviews > 0:
                average_ser_rating = round(
                    sum(r.rating for r in service_reviews)
                    / total_ser_reviews,
                    2
                )

            ser_reviews = [
                {
                    "rating": r.rating,
                    "review": r.review_text,
                    "total_review_users": total_ser_reviews
                }
                for r in service_reviews
            ]

            # Included Services
            include_services = (
                db.query(SubCategoryServices)
                .filter(
                    SubCategoryServices.sub_service_id == result.service_id
                )
                .all()
            )

            service_included = [
                {"name": inc.category.service_name}
                for inc in include_services
            ]

            service_booking_counts = (
                db.query(BookingDetails)
                .filter(BookingDetails.service_id == result.service_id)
                .count()
            )

            cart_id_exist = check_grooming_cart_service(
                db,
                user_id,
                franchise_id,
                sub.id
            )

            service_images = get_service_images(
                db=db,
                request=request,
                franchise_id=franchise_id,
                service_id=sub.id
            )

            services.append({
                "overal_rating": int(average_ser_rating),
                "package_type": sub.package_type,
                "package": "Package" if sub.package_type == 1 else "Service",
                "service_id": sub.id,
                "exist_cart_id": cart_id_exist,
                "total_service_bookings": service_booking_counts,
                "total_review_users": total_ser_reviews,
                "duration": sub.duration,
                "service_name": sub.service_name,
                "service_images": service_images,
                "price": float(sub.price) if sub.price else None,
                "services_included": service_included,
                "description": sub.description,
                "service_reviews": ser_reviews
            })

        # --------------------------------------------------
        # Booked Dates
        # --------------------------------------------------
        current_date = datetime.utcnow().date()

        booked_ids = (
            db.query(Bookings.booking_id)
            .filter(
                Bookings.franchise_id == franchise_id,
                Bookings.booking_status.in_([1, 2])
            )
            .all()
        )

        booked_ids = [b.booking_id for b in booked_ids]

        booked_dates_query = (
            db.query(BookingDetails)
            .filter(
                BookingDetails.booking_from >= current_date,
                BookingDetails.booking_id.in_(booked_ids)
            )
            .all()
        )

        booked_dates = [
            {
                "date": bd.booking_from.strftime("%Y-%m-%d"),
                "time": bd.booking_time.strftime("%I:%M %p")
            }
            for bd in booked_dates_query
        ]

        # --------------------------------------------------
        # Location Info
        # --------------------------------------------------
        franchise = db.query(Franchise).get(franchise_id)
        
        user_location = (
            db.query(UserLocation)
            .filter(UserLocation.user_id == user_id)
            .filter(UserLocation.is_primary == 1)
            .first()
        )

        if not user_location:
            raise HTTPException(status_code=400, detail="User location not found")

        # Distance Calculation
        distance_value = get_nearby_grooming(
            db=db,
            franchise_id=franchise.id,
            latitude=user_location.latitude,
            longitude=user_location.longitude
        )

        # Service Checking available
        check_service = checkDistanceRange(distance_value)

        location_info = {
            "franchise_id": franchise.id if franchise else None,
            "franchise_name": "petfirst",
            "image": build_full_url(request, franchise.image) if franchise else None,
            "location": franchise.location if franchise else None,
            "city": franchise.city if franchise else None,
            "state": franchise.state if franchise else None,
            "contact_number": franchise.contact_number if franchise else None,
            "pin_code": franchise.pin_code if franchise else None,
            "distance": f"{distance_value}(kms)" if distance_value else None,
            "serviceble": check_service,
            "rating": int(average_rating),
            "total_reviews": total_reviews,
            "total_franchise_bookings": booking_counts
        }

        return {
            "status": True,
            "service_type": 3,
            "services": services,
            "location": location_info,
            "reviews": reviews,
            "booked_dates": booked_dates,
            "exist_cart_services": exist_services,
            "message": "Franchise Grooming Details Info."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def check_grooming_cart_service(
    db: Session,
    user_id: int,
    franchise_id: int,
    service_id: int
):
    # -----------------------------------
    # Get Cart IDs for this user + franchise
    # -----------------------------------
    cart_ids = (
        db.query(GroomingCart.cart_id)
        .filter(
            GroomingCart.customer_id == user_id,
            GroomingCart.franchise_id == franchise_id
        )
        .all()
    )

    cart_ids = [c.cart_id for c in cart_ids]

    if not cart_ids:
        return None

    # -----------------------------------
    # Check if service exists in cart
    # -----------------------------------
    cart_detail = (
        db.query(GroomingCartDetails)
        .filter(
            GroomingCartDetails.cart_id.in_(cart_ids),
            GroomingCartDetails.service_id == service_id
        )
        .first()
    )

    if cart_detail:
        return cart_detail.cart_id

    return None

def get_service_images(
    db: Session,
    request: Request,
    franchise_id: int,
    service_id: int
):
    # Get package type
    package_type = (
        db.query(SubService.package_type)
        .filter(SubService.id == service_id)
        .scalar()
    )

    # Start base query (NO limit here)
    query = db.query(ServiceImages).filter(
        ServiceImages.service_id == service_id
    )

    # Apply conditions BEFORE limit
    if package_type == 1:
        query = query.filter(
            or_(
                ServiceImages.franchise_id == franchise_id,
                ServiceImages.franchise_id.is_(None)
            )
        )

    elif package_type == 2:
        query = query.filter(
            ServiceImages.franchise_id.is_(None)
        )

    # Order and limit LAST
    results = (
        query.order_by(ServiceImages.created_at.desc())
        .limit(6)
        .all()
    )

    if not results:
        return []

    base_url = str(request.base_url).rstrip("/")

    return [
        {
            "image": f"{base_url}/{res.image.lstrip('/')}" if res.image else None
        }
        for res in results
    ]


