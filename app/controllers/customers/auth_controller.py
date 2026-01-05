from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.customers.auth_schema import SendOTPRequest, ValidateOTPRequest
from app.services.customers.auth_service import send_otp, validate_otp
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def sendOTP(request: SendOTPRequest, db: Session = Depends(get_db)):
    return send_otp(db, request.mobile)

def validateOTP(request: ValidateOTPRequest, db: Session = Depends(get_db)):
    return validate_otp(db, request)
