# app/helpers/common.py

def rating_perc(count: int, total: int) -> int:
    if total == 0:
        return 0
    return round((count / total) * 100)


def format_time(time_obj):
    return time_obj.strftime("%I:%M %p") if time_obj else None


def checkDistanceRange(kms):
    if kms <= 15:
        return "yes"
    return "Not Serviceble"


from math import radians
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_service import FranchiseService

EARTH_RADIUS = 6371  # km

def get_nearby_franchise_info(
    db: Session,
    franchise_id: int,
    latitude: float,
    longitude: float,
    radius: int = 150
):
    lat = radians(latitude)
    lng = radians(longitude)

    distance_expr = (
        EARTH_RADIUS * func.acos(
            func.cos(lat)
            * func.cos(func.radians(Franchise.latitude))
            * func.cos(func.radians(Franchise.longitude) - lng)
            + func.sin(lat)
            * func.sin(func.radians(Franchise.latitude))
        )
    ).label("distance")

    result = (
        db.query(
            Franchise,
            distance_expr
        )
        .join(FranchiseService, FranchiseService.franchise_id == Franchise.id)
        .filter(Franchise.status_id == 1)
        .filter(Franchise.id == franchise_id)
        .filter(FranchiseService.service_type == 3)
        .order_by(distance_expr)
        .first()
    )

    if not result:
        return None

    franchise, distance = result

    return {
        "franchise": franchise,
        "distance": round(distance, 2)
    }


