from pydantic import BaseModel, Field, condecimal
from decimal import Decimal
from typing import Optional

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

class ValidateUserLocationRequest(BaseModel):
    location: str
    location_type: int
    address: str
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[int] = None
    is_primary: Optional[int] = None
    latitude: condecimal(max_digits=10, decimal_places=8)
    longitude: condecimal(max_digits=11, decimal_places=8)
