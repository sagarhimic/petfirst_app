from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class ValidatePetRequest(BaseModel):
    pet_type: int
    pet_name: str

    age_yr: int
    age_month: int
    dob: datetime

    breed: int
    color: int

    height: Decimal
    weight: int

    gender: int
    pet_profile_pic: str

    status: int
    is_primary: int
