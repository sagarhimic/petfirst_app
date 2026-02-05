from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class TrainerCart(Base):
    
    __tablename__ = "trainer_cart"
    
    cart_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer)
    service_type = Column(Integer)
    booking_date = Column(DateTime, nullable=True)
    booking_to = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    trainer_id = Column(Integer)
    customer_id = Column(Integer)
    pet_id = Column(Integer)
    total_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)


    # Relationships Used for trainer_cart Model

    # franchise = relationship("Franchise", back_populates="trainer_carts")

    # customer = relationship("User", back_populates="trainer_carts")

    # servicename = relationship("Services", back_populates="trainer_carts")

    # trainer_cart_details = relationship("TrainerCartDetails", back_populates="cart")