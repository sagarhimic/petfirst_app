from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.sms_template import SMSTemplate

def send_otp_sms(mobile: str, otp: str):
    db: Session = SessionLocal()

    try:
        # Fetch SMS template (same as Laravel)
        template = db.query(SMSTemplate).filter(SMSTemplate.id == 1).first()
        if not template:
            return False

        message = template.content.replace("{otp}", otp)

        # 🔁 Replace this with real SMS provider API
        print("📩 Sending SMS")
        print("To:", mobile)
        print("Message:", message)
        print("Purpose: PET OTP")

        return True

    finally:
        db.close()
