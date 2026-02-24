from sqlalchemy.orm import Session
from sqlalchemy import text
from math import radians
from sqlalchemy import func

from app.models.Franchises.franchise import Franchise
from app.models.Franchises.doctor_info import DoctorInfo
from app.models.Franchises.doctor import Doctor  # franchise_users table mapped as User

EARTH_RADIUS = 6371  # km


def get_nearby_doctor(
    db: Session,
    latitude: float,
    longitude: float,
    doctor_id: int | None = None,
    radius: int = 10
):
    """
    Equivalent to Laravel getNearbyDoctorLocations()
    """

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

    query = (
        db.query(
            Doctor.id.label("id"),
            Doctor.full_name.label("doctor_name"),
            Franchise.id.label("franchise_id"),
            Franchise.location,
            Franchise.city,
            Franchise.state,
            Franchise.latitude,
            Franchise.longitude,
            Franchise.contact_number,
            Franchise.pin_code,
            Doctor.mobile,
            Doctor.status,
            Doctor.profile_pic,
            DoctorInfo.specialization,
            DoctorInfo.exp,
            DoctorInfo.availability,
            DoctorInfo.consultation_fee,
            DoctorInfo.description,
            distance_expr
        )
        .join(DoctorInfo, DoctorInfo.doctor_id == Doctor.id)
        .join(Franchise, Franchise.id == DoctorInfo.franchise_id)
        .filter(Franchise.status_id == 1)
    )

    # Doctor filter (used in doctor details)
    if doctor_id:
        query = query.filter(Doctor.id == doctor_id)

    query = query.order_by(distance_expr)

    return query.all()
