from pydantic import BaseModel
from typing import Optional, List

class StorePetAdoptionRequest(BaseModel):
    full_name: str
    email: str
    mobile: str
    contact_method: int
    time_to_contact: int

class PetFilterRequest(BaseModel):
    pet_types: List[int] = []
    size: List[int] = []
    gender: List[int] = []
    breeds: List[int] = []
    colors: List[int] = []
    age: Optional[str] = None
    latitude: float
    longitude: float



