from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class TrainerPersonalInfo(Base):
    __tablename__ = "trainer_personal_info"
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    full_name = Column(String(125))
    email = Column(String(125))
    gender = Column(Integer)
    exp = Column(String(125))
    profile_pic = Column(Text)
    about = Column(Text)
    price = Column(Numeric(10, 0), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(10, 8), nullable=True)
    city = Column(String(125))
    state = Column(String(125))
    country = Column(String(125))
    location = Column(Text)
    pincode = Column(String(20))
    certificate = Column(Text)
    aadhar_front = Column(Text)
    aadhar_back = Column(Text)
    availability = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    trainer = relationship("Trainer", back_populates="personal_info")
