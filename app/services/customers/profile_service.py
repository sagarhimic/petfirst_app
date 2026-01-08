from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from app.models.user import User
from app.models.user_personal_info import UserPersonalInfo
from app.models.user_location import UserLocation
from datetime import datetime

def get_profile_service(db: Session, user_id: int, request: Request):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"status": False, "message": "Access Denied"}

    user_info = (
        db.query(UserPersonalInfo)
        .filter(UserPersonalInfo.user_id == user_id)
        .first()
    )

    profile_pic_url = None
    if user_info and user_info.profile_pic:
        profile_pic_url = str(request.base_url) + user_info.profile_pic.lstrip("/")

    return {
        "status": True,
        "message": "Profile Info.",
        "data": {
            "user_id": user.id,
            "mobile": user.mobile or (user_info.mobile if user_info else ""),
            "name": user.name,
            "email": (
                user_info.email if user_info and user_info.email
                else user.email
            ),
            "gender_id": user_info.gender if user_info else "",
            "gender": (
                user_info.genderinfo.name
                if user_info and user_info.genderinfo
                else None
            ),
            "profile_pic": profile_pic_url,
            "role_id": user.role_id,
            "status": user.status,
            "access_for": user.access_for
        }
    }


def store_user_location_service(
    db: Session,
    data: dict,
    user_id: int,
):
    try:
        # 🔐 BEGIN TRANSACTION
         # ✅ FIX HERE
        if data.is_primary == 1:
            db.query(UserLocation).filter(
                UserLocation.user_id == user_id,
                UserLocation.is_primary == 1
            ).update({"is_primary": None})

        location = UserLocation(
            user_id=user_id,
            location=data.location,
            location_type=data.location_type,
            address=data.address,
            country=data.country,
            city=data.city,
            state=data.state,
            pin_code=data.pin_code,
            is_primary=data.is_primary,
            latitude=data.latitude,
            longitude=data.longitude,
            created_at=datetime.utcnow(),
            created_by=user_id
        )

        db.add(location)
        db.flush()  # ✅ get pet.id before commit
        db.commit()

        return {
            "status": True,
            "pet_id": location.location_id,
            "message": "Location added successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
