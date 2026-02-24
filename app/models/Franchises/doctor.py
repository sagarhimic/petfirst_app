from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Doctor(Base):
    __tablename__ = "franchise_users"

    id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer)
    user_type = Column(Integer)
    full_name = Column(String(125))
    city = Column(String(125))
    state = Column(String(125))
    country = Column(Integer)
    state_id = Column(Integer)
    country_id = Column(Integer)
    mobile = Column(String(125))
    role_id = Column(Numeric(10, 8), nullable=True)
    email = Column(String(125))
    password = Column(String(255))
    status = Column(Integer)
    address = Column(Text)
    logged_in = Column(Integer)
    profile_pic = Column(Text)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    bookings = relationship(
        "Bookings",
        foreign_keys="Bookings.doctor_id",
        back_populates="doctor"
    )

