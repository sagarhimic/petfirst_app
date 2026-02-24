# app/models/events/event.py

from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Float, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)  # 1 = Event, 2 = Activity
    name = Column(String(125))
    about = Column(Text)
    event_date = Column(DateTime)
    event_time_from = Column(String(55))
    event_time_to = Column(String(55))
    location = Column(String(100))
    city = Column(String(125))
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    pincode = Column(Integer)
    entry_fee = Column(Numeric(10, 2))
    discount = Column(Float)
    status_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    created_by = Column(Integer)
    updated_by = Column(Integer)

    # -----------------------------
    # Relationships (Laravel style)
    # -----------------------------
    gallery = relationship(
        "EventGallery",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    benefits = relationship(
        "EventBenefit",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    state = relationship("State")
    
    country = relationship("Country")
