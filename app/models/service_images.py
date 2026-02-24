from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class ServiceImages(Base):
    
    __tablename__ = "service_images"
    
    id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer)
    service_id = Column(
        Integer,
        ForeignKey("sub_services.id")  # ✅ VERY IMPORTANT
    )
    user_type = Column(Integer)
    image = Column(Text)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)