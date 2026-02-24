from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class BookingHistoryReschedule(Base):
    
    __tablename__ = "booking_history_reschedule"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    booking_from = Column(DateTime, nullable=True)
    booking_to = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)