from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.SMS.sms_template import SMSTemplate
from app.services.SMS.sms_service import SMSHorizonService
from app.models.SMS.sms_template import SMSTemplate

def send_otp_sms(mobile: str, otp: str):
    db: Session = SessionLocal()

    try:
        sms_template = db.query(SMSTemplate).filter(
        SMSTemplate.id == 1
        ).first()

        if not sms_template:
            return {"error": "Template not found"}

        text = sms_template.content.replace("{otp}", otp)

        response = SMSHorizonService.send_sms(
            db=db,
            params={
                "mobile": mobile,
                "message": text,
                "purpose": "PET OTP",
                "sms_template_id": sms_template.id,
                "receiver_name": mobile
            },
            auth_user=None  # pass current user if needed
        )

        return {"response": response}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
