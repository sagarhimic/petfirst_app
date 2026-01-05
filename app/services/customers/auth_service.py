from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_otp import UserOTP
from app.models.user_personal_info import UserPersonalInfo
from app.models.pet_info import PetInfo
from app.core.security import create_token
import random
from sqlalchemy import desc
from app.services.customers.device_service import save_device_details
from app.utils.sms import send_otp_sms


def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(db: Session, mobile: str):
    db.query(UserOTP).filter(UserOTP.user_id == mobile).delete()

    otp = "2556" if mobile in ["2222222222", "3333333333"] else generate_otp()

    db.add(UserOTP(user_id=mobile, otp=otp))
    db.commit()

    masked = "x" * (len(mobile)-4) + mobile[-4:]

    send_otp_sms(mobile, otp)

    return {
        "status": True,
        "message": {
            "mobile": mobile,
            "otp": otp,
            "success_meessage": f"OTP sent to-{masked}"
        }
    }

def validate_otp(db: Session, data):
    otp_row = (
        db.query(UserOTP)
        .filter(
            UserOTP.user_id == data.mobile)
        .order_by(desc(UserOTP.created_at))
        .first()
    )

    print("DB OTP:", otp_row.otp)
    print("REQ OTP:", data.mobile_otp)

    if not otp_row:
        return {"status": False, "message": "OTP expired or not found."}

    # ✅ SAFE string comparison
    if str(otp_row.otp).strip() != str(data.mobile_otp).strip():
        return {"status": False, "message": "OTP not matched."}

    # delete OTP after success
    db.delete(otp_row)
    db.commit()

    user = db.query(User).filter(User.mobile == data.mobile).first()

    if not user:
        user = User(
            mobile=data.mobile,
            login_type=data.login_type,
            role_id=2,
            status=1
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 🔽 SAVE DEVICE ONLY FOR MOBILE LOGIN
    if data.login_type == 1:
        save_device_details(db, data, user.id)

    register_key = db.query(UserPersonalInfo).filter(UserPersonalInfo.user_id == user.id).first()
    pet_info_key = db.query(PetInfo).filter(PetInfo.owner_id == user.id).first()

    token = create_token(user.id)

    return {
        "status": True,
        "message": "Successfully logged in.",
        "token": token,
        "data": {
            "user_id": user.id,
            "name": user.name,
            "mobile": user.mobile,
            "access_for": user.access_for,
            "register_key": 1 if register_key else None,
            "pet_info_key": 1 if pet_info_key else None
        }
    }
