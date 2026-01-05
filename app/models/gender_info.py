from sqlalchemy import Column, Integer, String
from app.core.database import Base

class GenderInfo(Base):
    __tablename__ = "gender_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(125), nullable=True)