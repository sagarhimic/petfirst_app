from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

from app.models.gender_info import GenderInfo  # ✅ IMPORTANT

class UserPersonalInfo(Base):
    __tablename__ = "user_personal_info"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    full_name = Column(String(125), nullable=True)
    email = Column(String(125), nullable=True)

    # 🔑 Foreign Key
    gender = Column(Integer, ForeignKey("gender_types.id"), nullable=True)

    profile_pic = Column(Text, nullable=True)

    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🔗 Relationship (INSIDE class)
    genderinfo = relationship(
        "GenderInfo",
        backref="user_personal_info",
        lazy="joined"
    )

    user = relationship(
        "User",
        back_populates="userinfo"
    )
