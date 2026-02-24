
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.SMS.sms_template import SMSTemplate
from app.models.SMS.sms_log import SMSLog


class SMSHorizonService:

    @staticmethod
    def send_sms(db: Session, params: dict, auth_user=None):

        sms_template = db.query(SMSTemplate).filter(
            SMSTemplate.id == params["sms_template_id"]
        ).first()

        if not sms_template:
            return {"error": "SMS Template not found"}

        url = "http://smshorizon.co.in/api/sendsms.php"

        post_params = {
            "apikey": "pW5OInRdH1gjxbXRTTKO--test",
            "user": "pipip--test",
            "senderid": "USMSTR",
            "type": sms_template.text_type,
            "tid": sms_template.dlt_template_id,
            "mobile": params["mobile"],
            "message": params["message"]
        }

        try:
            response = requests.post(url, data=post_params, timeout=10)
            response_text = response.text.strip()

        except Exception as e:
            return {"error": str(e)}

        status = response_text

        if response_text.isnumeric():
            status = SMSHorizonService.get_sms_status(response_text)

        log = SMSLog(
            purpose=params.get("purpose", ""),
            sender_id=getattr(auth_user, "id", 1) if auth_user else 1,
            sender_name=getattr(auth_user, "name", "Admin") if auth_user else "Admin",
            receiver_name=params.get("receiver_name", "Admin"),
            receiver_mobile=params["mobile"],
            user_id=None,
            message=params["message"],
            response_id=response_text,
            status=status,
            vendor=1,
            sms_type=1,
            count=len(params["mobile"].split(",")),
            sms_count=None,
            created_at=datetime.utcnow()
        )

        db.add(log)
        db.commit()

        return response_text

    @staticmethod
    def get_sms_status(msgid: str):

        url = "http://smshorizon.co.in/api/deliveryreport.php"
        username = "pipip--test"
        api_key = "pW5OInRdH1gjxbXRTTKO--test"

        request_url = f"{url}?user={username}&apikey={api_key}&msgid={msgid}"

        try:
            response = requests.get(request_url, timeout=10)
            return response.text.strip()   # ✅ MUST RETURN

        except Exception as e:
            return str(e)