from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class FranchiseServiceReview(Base):
    __tablename__ = "franchise_service_reviews"

    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    franchise_id = Column(Integer)
    service_id = Column(Integer)
    rating = Column(Float)
    review_text = Column(Text)
    review_date = Column(DateTime, nullable=True, default=datetime.utcnow)

    # Relationship to User
    user = relationship("User", back_populates="service_reviews")

