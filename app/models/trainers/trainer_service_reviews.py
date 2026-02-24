from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class TrainerServiceReview(Base):
    __tablename__ = "trainer_service_reviews"

    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    service_id = Column(Integer, ForeignKey("sub_services.id"), nullable=True)
    rating = Column(Float)
    review_text = Column(Text)
    review_date = Column(Date, nullable=True, default=date.today
)


    trainer = relationship(
        "Trainer",
        back_populates="trainer_service_reviews"
    )

    customer = relationship(
        "User",
        back_populates="trainer_service_reviews"
    )

    service = relationship("SubService", back_populates="trainer_service_reviews")