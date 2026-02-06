from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric, Time, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class DoctorReview(Base):
    __tablename__ = "doctor_reviews"

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer)
    franchise_id = Column(Integer)
    user_id = Column(Integer)
    doctor_id = Column(Integer)
    rating = Column(String(125))
    review_text = Column(Text)
    review_date = Column(DateTime, nullable=True, default=datetime.utcnow)
