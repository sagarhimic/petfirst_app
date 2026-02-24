# app/models/events/event_benefit.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class EventBenefit(Base):
    __tablename__ = "event_benefits"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    benefit_name = Column(String(125))
    status_id = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    event = relationship("Event", back_populates="benefits")
