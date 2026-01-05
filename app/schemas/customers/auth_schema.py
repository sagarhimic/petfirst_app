from pydantic import BaseModel
from typing import Optional

class SendOTPRequest(BaseModel):
    mobile: str

class ValidateOTPRequest(BaseModel):
    mobile: str
    mobile_otp: str
    login_type: int
    device_type: Optional[str] = None
    device_id: Optional[str] = None
    device_model: Optional[str] = None
    device_software: Optional[str] = None
    device_manufacturer: Optional[str] = None
    brand: Optional[str] = None
    fcm_token: Optional[str] = None
    app_version: Optional[str] = None
