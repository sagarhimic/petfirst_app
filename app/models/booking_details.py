from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class BookingDetails(Base):
    
    __tablename__ = "booking_details"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    service_id = Column(Integer)
    event_id = Column(Integer, ForeignKey("events.id"))
    doctor_id = Column(Integer)
    amount = Column(Numeric(10, 2), nullable=True)
    booking_from = Column(DateTime, nullable=True)
    booking_to = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    quantity = Column(Integer)
    status = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    # ✅ Event relation
    eventname = relationship(
        "Event",
        primaryjoin="BookingDetails.event_id == foreign(Event.id)",
        uselist=False,
        viewonly=True
    )

    service = relationship(
        "SubService",
        primaryjoin="BookingDetails.service_id == foreign(SubService.id)",
        uselist=False,
        viewonly=True

    )
