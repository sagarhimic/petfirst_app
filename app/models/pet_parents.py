from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class PetParents(Base):
    __tablename__ = "pet_parents"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pet_info.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    pet_name = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    mobile = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)

    state_id = Column(Integer, nullable=True)
    city = Column(String(255), nullable=True)
    country_id = Column(Integer,  nullable=True)
    pincode = Column(String(20), nullable=True)
    gender = Column(Integer,  nullable=True)
    parent_type = Column(Integer, nullable=True)
    status = Column(Integer, default=1)

    created_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
  #  pet = relationship("PetInfo", back_populates="parents")
    createdby = relationship("User", foreign_keys=[created_by])
    updatedby = relationship("User", foreign_keys=[updated_by])
 #   genderinfo = relationship("Gender")
 #   country = relationship("Country")
 #   state = relationship("State")
