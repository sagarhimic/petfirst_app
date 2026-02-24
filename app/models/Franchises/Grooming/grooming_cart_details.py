from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class GroomingCartDetails(Base):
    
    __tablename__ = "grooming_cart_details"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("grooming_cart.cart_id"))  # FK to grooming_cart.cart_id
    service_id = Column(
        Integer,
        ForeignKey("sub_services.id"),   # ✅ THIS WAS MISSING
        nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=True)
    booking_from = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    status = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    # ✅ FIXED
    cart = relationship(
        "GroomingCart",
        back_populates="cartDetails"
    )

    servicetemp = relationship(
        "SubService",
        back_populates="cartserv"
    )
