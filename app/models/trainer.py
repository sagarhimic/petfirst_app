from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    name = Column(String(125))
    mobile = Column(String(125))
    email = Column(String(125))
    password = Column(String(125))
    logged_in = Column(Integer)
    user_token = Column(String)
    token_expiration = Column(String(125))
    status = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_logged_in_at = Column(DateTime, nullable=True)

    personal_info = relationship("TrainerPersonalInfo", back_populates="trainer")

    bookings = relationship("Bookings", back_populates="trainer")

    trainer_service_reviews = relationship(
        "TrainerServiceReview",
        back_populates="trainer"
    )
