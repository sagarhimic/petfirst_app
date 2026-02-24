from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Numeric,
    Index
)
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User
from app.models.pet_types import PetTypes
from app.models.breeds import Breeds
from app.models.colors import Colors
from app.models.gender_info import GenderInfo
from datetime import datetime

class PetInfo(Base):
    __tablename__ = "pet_info"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, nullable=True, index=True)
    pet_type = Column(Integer, nullable=True)

    pet_name = Column(String(125), nullable=True)

    age_yr = Column(Integer, nullable=True)
    age_month = Column(Integer, nullable=True)

    dob = Column(DateTime, nullable=True)

    breed = Column(Integer, nullable=True, index=True)
    color = Column(Integer, nullable=True)

    height = Column(Numeric(10, 2), nullable=True)
    weight = Column(Integer, nullable=True)

    gender = Column(Integer, nullable=True, index=True)

    is_primary = Column(Integer, nullable=True)

    pet_profile_pic = Column(Text, nullable=True)

    status = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)

    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    bookings = relationship(
        "Bookings",
        foreign_keys="Bookings.pet_id",
        back_populates="pet"
    )

# Optional explicit indexes (already covered by index=True above)
Index("idx_pet_info_owner_id", PetInfo.owner_id)
Index("idx_pet_info_gender", PetInfo.gender)
Index("idx_pet_info_breed", PetInfo.breed)


