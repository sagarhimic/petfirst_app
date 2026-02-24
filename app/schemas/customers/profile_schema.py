from pydantic import BaseModel
from typing import Optional

class ValidateProfileRequest(BaseModel):
    full_name:str
    mobile:str
    email:str
    gender:int
    location:str
    location_type:int
    address:Optional[str] = None
    country:Optional[str] = None
    city:Optional[str] = None
    state:Optional[str] = None
    pin_code:Optional[str] = None
    is_primary:int
    latitude:Optional[str] = None
    longitude:Optional[str] = None
    access_for:int

class ModifyProfileNameRequest(BaseModel):
    full_name:str

class UpdateProfilePicRequest(BaseModel):
    profile_pic:str




