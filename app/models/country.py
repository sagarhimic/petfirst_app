
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(125))
    country_code = Column(String(125))
    phone_code = Column(String(125))
    region = Column(String(125))
    is_active = Column(Integer)
