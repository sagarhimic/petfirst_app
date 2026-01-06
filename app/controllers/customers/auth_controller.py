from fastapi import Depends, Form
from sqlalchemy.orm import Session
from app.schemas.customers.auth_schema import ValidateOTPRequest
from app.services.customers.auth_service import send_otp, validate_otp
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def sendOTP(request: SendOTPRequest = Depends(), db: Session = Depends(get_db)):
def sendOTP(
    mobile: str = Form(...),   # 👈 IMPORTANT
    db: Session = Depends(get_db)
):
    return send_otp(db, mobile)

# def validateOTP(request: ValidateOTPRequest = Depends(), db: Session = Depends(get_db)):
def validateOTP(
    mobile: str = Form(...),
    mobile_otp: str = Form(...),
    login_type: int = Form(...),

    device_type: str | None = Form(None),
    device_id: str | None = Form(None),
    device_model: str | None = Form(None),
    device_software: str | None = Form(None),
    device_manufacturer: str | None = Form(None),
    brand: str | None = Form(None),
    fcm_token: str | None = Form(None),
    app_version: str | None = Form(None),

    db: Session = Depends(get_db)
):
    data = ValidateOTPRequest(
        mobile=mobile,
        mobile_otp=mobile_otp,
        login_type=login_type,
        device_type=device_type,
        device_id=device_id,
        device_model=device_model,
        device_software=device_software,
        device_manufacturer=device_manufacturer,
        brand=brand,
        fcm_token=fcm_token,
        app_version=app_version
    )
    return validate_otp(db, data)
