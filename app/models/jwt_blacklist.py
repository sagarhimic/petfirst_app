from sqlalchemy import Column, Integer, Text, DateTime
from app.core.database import Base
from datetime import datetime

class JWTBlacklist(Base):
    __tablename__ = "jwt_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
