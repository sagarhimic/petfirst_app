from pydantic import BaseModel, EmailStr
from typing import Optional

class StorePetParentRequest(BaseModel):
    pet_id: int
    pet_parent_name: str
    parent_owner_name: str
    parent_mobile: str
    parent_email: EmailStr
    address: str
    state_id: int
    city: str
    country_id: int
    pincode: str
    parent_type: int

class UpdatePetParentRequest(BaseModel):
    pet_id: int
    pet_parent_name: str
    pet_parent_owner_name: str
    parent_mobile: str
    parent_email: EmailStr
    address: str
    state_id: int
    city: str
    country_id: int
    pincode: str
    parent_type: int