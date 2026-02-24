from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric, Time, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class DoctorGallery(Base):
    __tablename__ = "doctor_gallery"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    image = Column(Text)
    status_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
