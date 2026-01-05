from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class UserOTP(Base):
    __tablename__ = "user_otp"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(15))
    otp = Column(String(6))
    type = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
