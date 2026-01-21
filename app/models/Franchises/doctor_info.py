from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric, Time, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class DoctorInfo(Base):
    __tablename__ = "doctor_info"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    franchise_id = Column(Integer)
    gender = Column(Integer)
    specialization = Column(String(255))
    exp = Column(String(125))
    consultation_fee = Column(Numeric(10, 2), nullable=True)
    description = Column(Text)
    availability_from = Column(Time)
    availability_to = Column(Time)
    availability = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
