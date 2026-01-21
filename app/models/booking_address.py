from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time
from app.core.database import Base

class BookingAddress(Base):
    
    __tablename__ = "booking_address"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    customer_id = Column(Integer)
    location_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
