from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time
from app.core.database import Base

class UserService(Base):
    __tablename__ = "assign_trainer_services"
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer)
    service_id = Column(Integer, ForeignKey("trainers.id"))
    duration = Column(Text)
    price = Column(Numeric(10, 2), nullable=True)
    status = Column(Integer)
    approved_by = Column(Integer)
    approve_status = Column(Integer)
    approved_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    description = Column(Text)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
