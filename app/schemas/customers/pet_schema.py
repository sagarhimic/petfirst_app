from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class ValidatePetRequest(BaseModel):
    pet_type: int
    pet_name: str

    age_yr: Optional[int] = None
    age_month: Optional[int] = None
    dob: Optional[datetime] = None

    breed: int
    color: int

    height: Decimal
    weight: int

    gender: int
    is_primary: Optional[int] = None

    class Config:
        extra = "forbid"  # ❗ Reject unexpected fields

class UpdatePetRequest(BaseModel):
    pet_type: int
    pet_name: str

    age_yr: Optional[int] = None
    age_month: Optional[int] = None
    dob: Optional[datetime] = None

    breed: int
    color: int

    height: Decimal
    weight: int
    gender: int

    is_primary: Optional[int] = None

class PetUpdatePrimaryRequest(BaseModel):
    pet_id: int
