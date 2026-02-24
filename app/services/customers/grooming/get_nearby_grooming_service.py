from sqlalchemy.orm import Session
from sqlalchemy import text
from math import radians
from sqlalchemy import func

from app.models.Franchises.franchise import Franchise
from app.models.Franchises.franchise_service import FranchiseService

EARTH_RADIUS = 6371  # km


def get_nearby_grooming(
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
        db.query(distance_expr)
        .join(FranchiseService, FranchiseService.franchise_id == Franchise.id)
        .filter(Franchise.status_id == 1)
        .filter(Franchise.id == franchise_id)
        .filter(FranchiseService.service_type == 3)
        .order_by(distance_expr)
        .first()
    )

    if result:
        return round(result[0], 2)

    return None

