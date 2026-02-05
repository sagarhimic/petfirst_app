from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class TrainerCartDetails(Base):
    
    __tablename__ = "trainer_cart_details"
    
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("trainer_cart.cart_id"))
    service_id = Column(Integer)
    event_id = Column(Integer)
    amount = Column(Numeric(10, 2))
    booking_from = Column(DateTime)
    booking_to = Column(DateTime)
    booking_time = Column(Time)
    quantity = Column(Integer)
    status = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)


    # Relationships Used for trainer_cart Model

    # eventname = relationship("Events", back_populates="trainer_cart_details")

    # cart = relationship("TrainerCart", back_populates="trainer_cart_details")

    # service = relationship(
    #     "UserService",
    #     primaryjoin="foreign(TrainerCartDetails.service_id) == UserService.service_id",
    #     viewonly=True
    # )


    

