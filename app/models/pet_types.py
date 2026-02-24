from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class PetTypes(Base):
    __tablename__ = "pet_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=True)
    status = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)