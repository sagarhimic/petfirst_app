from sqlalchemy.orm import Session
from fastapi import Request
from app.models.user import User
from app.models.user_personal_info import UserPersonalInfo

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
