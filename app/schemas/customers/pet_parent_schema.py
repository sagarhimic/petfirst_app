from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import Field


class StorePetParentRequest(BaseModel):
    pet_id: int
    pet_parent_name: str
    parent_owner_name: str
    parent_mobile: str = Field(..., min_length=10, max_length=10)
    parent_email: EmailStr
    address: str
    state_id: int
    city: str
    country_id: int
    pincode: str = Field(..., min_length=6, max_length=6)
    parent_type: int


class UpdatePetParentRequest(BaseModel):
    pet_id: Optional[int] = None
    pet_parent_name: Optional[str] = None
    parent_owner_name: Optional[str] = None
    parent_mobile: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    address: Optional[str] = None
    state_id: Optional[int] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    pincode: Optional[str] = None
    parent_type: Optional[int] = None
