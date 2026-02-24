from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class GroomingCart(Base):
    
    __tablename__ = "grooming_cart"
    
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    franchise_id = Column(Integer)
    service_type = Column(Integer)
    booking_date = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    assign_user_id = Column(Integer)
    customer_id = Column(Integer)
    pet_id = Column(Integer)
    total_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    cartDetails = relationship(
        "GroomingCartDetails",
        back_populates="cart",
        cascade="all, delete-orphan"
    )
