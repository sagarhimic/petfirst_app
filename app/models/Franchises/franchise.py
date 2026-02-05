from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Franchise(Base):
    __tablename__ = "franchises"

    id = Column(Integer, primary_key=True)
    franchise_unique_id = Column(String(125))
    location = Column(Text)
    address = Column(Text)
    city = Column(String(125))
    state = Column(String(125))
    country = Column(Integer)
    state_id = Column(Integer)
    country_id = Column(Integer)
    pin_code = Column(String(45))
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(10, 8), nullable=True)
    contact_person = Column(String(125))
    contact_number = Column(String(125))
    office_phone = Column(String(125))
    delivery_radius = Column(Numeric(10, 0), nullable=True)
    status_id = Column(Integer)
    comment = Column(Text)
    image = Column(String(256))
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    bookings = relationship("Bookings", back_populates="franchise")

    # trainer_carts = relationship(
    #     "TrainerCart",
    #     back_populates="franchise",
    #     cascade="all, delete-orphan"
    # )
