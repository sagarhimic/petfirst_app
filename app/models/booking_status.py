from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class BookingStatus(Base):
    
    __tablename__ = "booking_statuses"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status_id = Column(Integer)
    color_code = Column(String(20))
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    bookings = relationship("Bookings", back_populates="bookingstatus")