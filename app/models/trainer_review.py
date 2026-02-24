from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class TrainerReview(Base):
    __tablename__ = "trainer_reviews"

    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    rating = Column(Float)
    review_text = Column(Text)
    review_date = Column(Date, nullable=True, default=date.today
)

# 🔁 Relationships

    # trainer = relationship(
    #     "TrainerUser",
    #     back_populates="trainer_reviews"
    # )

    # customer = relationship(
    #     "User",
    #     back_populates="trainer_reviews"
    # )

    # service_name = relationship(
    #     "SubService",
    #     back_populates="trainer_reviews"
    # )