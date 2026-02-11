from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from app.core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class UserLocation(Base):
    __tablename__ = "user_locations"

    location_id = Column(Integer, primary_key=True, index=True)
   # user_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(125))
    location_type = Column(Integer)
    address = Column(String(125))
    country = Column(String(125))
    city = Column(String(125))
    state = Column(String(125))
    pin_code = Column(Integer)
    is_primary = Column(Integer)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(10, 8), nullable=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="locations")

