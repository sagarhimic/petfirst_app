from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class Events(Base):
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    name = Column(String(125))
    about = Column(Text)
    event_date = Column(DateTime, nullable=True)
    event_time_from = Column(String(55))
    event_time_to = Column(String(55))
    location = Column(String(100))
    city = Column(String(125))
    state_id = Column(Integer)
    country_id = Column(Integer)
    pincode = Column(Numeric(10, 0), nullable=True)
    entry_fee = Column(Numeric(10, 2), nullable=True)
    discount= Column(Numeric(10, 2), nullable=True)
    status_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)


