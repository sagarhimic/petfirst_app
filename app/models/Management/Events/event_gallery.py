from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class EventGallery(Base):
    
    __tablename__ = "event_gallery"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    image = Column(String(125))
    status_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)