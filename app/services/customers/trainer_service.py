# app/services/trainer_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.trainer import Trainer
from app.models.trainer_personal_info import TrainerPersonalInfo
from app.models.trainer_review import TrainerReview
from app.models.bookings import Bookings
from app.models.trainers.assign_trainer_service import UserService

EARTH_RADIUS = 6371  # km


def get_nearby_trainer_locations(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    service_id: int | None,
    trainer_id: int | None,
):
    lat = func.radians(latitude)
    lng = func.radians(longitude)

    distance = (
        EARTH_RADIUS
        * func.acos(
            func.cos(lat)
            * func.cos(func.radians(TrainerPersonalInfo.latitude))
            * func.cos(func.radians(TrainerPersonalInfo.longitude) - lng)
            + func.sin(lat)
            * func.sin(func.radians(TrainerPersonalInfo.latitude))
        )
    ).label("distance")

    subquery = (
        db.query(
            Trainer.id.label("id"),  # ✅ IMPORTANT FIX
            Trainer.name.label("trainer_name"),
            Trainer.mobile,
            Trainer.status,
            TrainerPersonalInfo.location,
            TrainerPersonalInfo.profile_pic,
            TrainerPersonalInfo.exp,
            distance,
        )
        .join(TrainerPersonalInfo, TrainerPersonalInfo.trainer_id == Trainer.id)
        .filter(Trainer.status == 1)
        .filter(TrainerPersonalInfo.availability.is_(None))
    )

    if trainer_id:
        subquery = subquery.filter(Trainer.id == trainer_id)

    if service_id:
        subquery = subquery.filter(
            Trainer.id.in_(
                db.query(UserService.trainer_id)
                .filter(UserService.service_id == service_id)
                .filter(UserService.status == 1)
            )
        )

    subquery = subquery.subquery()

    return (
        db.query(subquery)
        .filter(subquery.c.distance <= radius)
        .order_by(subquery.c.distance)
        .all()
    )

def get_trainers_service(
    db: Session,
    data: dict
):
    radius = 150

    nearby_trainers = get_nearby_trainer_locations(
        db=db,
        latitude=data.latitude,
        longitude=data.longitude,
        radius=radius,
        service_id=data.service_id,
        trainer_id=data.trainer_id,
    )

    trainers = []

    for trainer in nearby_trainers:
        reviews = (
            db.query(TrainerReview.rating)
            .filter(TrainerReview.trainer_id == trainer.id)  # ✅ works now
            .all()
        )

        booking_count = (
            db.query(Bookings)
            .filter(Bookings.trainer_id == trainer.id)
            .filter(Bookings.booking_status == 4)
            .count()
        )

        ratings = [r.rating for r in reviews]
        total_reviews = len(ratings)

        average_rating = (
            round(sum(ratings) / total_reviews, 2)
            if total_reviews > 0
            else 0
        )

        trainers.append({
            "trainer_id": trainer.id,
            "name": trainer.trainer_name,
            "mobile": trainer.mobile,
            "profile_pic": trainer.profile_pic,
            "location": trainer.location,
            "exp": trainer.exp or 0,
            "distance": f"{round(trainer.distance, 2)}(kms)",
            "rating": int(average_rating),
            "total_reviews": total_reviews,
            "total_bookings": booking_count,
            "status": "Available" if trainer.status == 1 else "Not Available",
        })

    return trainers

