from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, UploadFile
from app.models.user import User
from app.models.user_personal_info import UserPersonalInfo
from app.models.user_location import UserLocation
from datetime import datetime
import os, shutil

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
def modify_profile_name_service(db: Session, user_id: int, payload):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"status": False, "message": "Access Denied"}

    user.name = payload.full_name
    
    user_info = (
        db.query(UserPersonalInfo)
        .filter(UserPersonalInfo.user_id == user_id)
        .first()
    )

    if not user_info:
        user_info = UserPersonalInfo(user_id=user_id)
        db.add(user_info)

    user_info.full_name = payload.full_name
    user_info.updated_at = datetime.utcnow()
    user_info.updated_by = user_id

    db.commit()

    return {
        "status": True,
        "message": "Profile name updated successfully"
    }

def update_profile_pic_service(db: Session, user_id: int, profile_pic: UploadFile):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"status": False, "message": "Access Denied"}

    user_info = (
        db.query(UserPersonalInfo)
        .filter(UserPersonalInfo.user_id == user_id)
        .first()
    )

    if not user_info:
        user_info = UserPersonalInfo(user_id=user_id)
        db.add(user_info)

    # If no file uploaded, just update metadata and exit
    if not profile_pic:
        db.commit()
        return {"status": True, "message": "Profile updated"}

    ext = profile_pic.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "pdf"]:
        return {"status": False, "message": "Invalid file type"}

    folder = f"uploads/customers/owners/{user_id}/{datetime.now().strftime('%Y/%m')}"
    os.makedirs(folder, exist_ok=True)

    filename = f"pro_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file_path = f"{folder}/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(profile_pic.file, buffer)

    user_info.profile_pic = file_path
    user_info.updated_at = datetime.utcnow()
    user_info.updated_by = user_id

    db.commit()

    return {"status": True, "message": "Profile picture updated successfully"}

def get_locations_service(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"status": False, "message": "Access Denied"}

    locations = (
        db.query(UserLocation)
        .filter(UserLocation.user_id == user_id)
        .all()
    )

    location_list = []
    for loc in locations:
        location_list.append({
            "location_id": loc.location_id,
            "location": loc.location,
            "location_type": loc.location_type,
            "address": loc.address,
            "country": loc.country,
            "city": loc.city,
            "state": loc.state,
            "pin_code": loc.pin_code,
            "is_primary": loc.is_primary,
            "latitude": str(loc.latitude),
            "longitude": str(loc.longitude),
        })

    return {
        "status": True,
        "message": "User Locations fetched successfully",
        "data": location_list
    }

def location_update_primary_service(db: Session, user_id: int, location_id: int):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    # Step 1: Set selected location as primary
    update_primary = (
        db.query(UserLocation)
        .filter(UserLocation.user_id == user_id,
                UserLocation.location_id == location_id)
        .update({"is_primary": 1})
    )

    if update_primary > 0:
        # Step 2: Reset other locations
        (
            db.query(UserLocation)
            .filter(UserLocation.user_id == user_id,
                    UserLocation.location_id != location_id)
            .update({"is_primary": None})
        )

    db.commit()

    return {"status": True}


def delete_location_service(db: Session, user_id: int, location_id: int):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        # Delete the record
        (
            db.query(UserLocation)
            .filter(UserLocation.location_id == location_id,
                    UserLocation.user_id == user_id)
            .delete()
        )

        db.commit()

        return {"status": True, "message": "Location deleted successfully."}

    except Exception as e:
        db.rollback()
        return {
            "status": False,
            "message": "Something went wrong.",
            "errors": str(e)
        }

