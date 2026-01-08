from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time
from app.core.database import Base

class Bookings(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("trainers.id"))
    service_type = Column(Integer)
    booking_type = Column(Integer)
    booking_date = Column(DateTime, nullable=True)
    booking_to = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    trainer_id = Column(Integer)
    customer_id = Column(Integer)
    pet_id = Column(Integer)
    doctor_id = Column(Integer)
    total_amount = Column(Numeric(10, 2), nullable=True)
    discount = Column(Numeric(10, 2), nullable=True)
    gst= Column(Numeric(10, 2), nullable=True)
    sgst= Column(Numeric(10, 2), nullable=True)
    service_tax  = Column(Numeric(10, 2), nullable=True)
    booking_status = Column(Integer)
    sub_status_id = Column(Integer)
    cancel_reason = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
