# app/models/events/event_gallery.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class EventGallery(Base):
    __tablename__ = "event_gallery"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    image = Column(String(255))
    status_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    # Relationship
    event = relationship("Event", back_populates="gallery")
