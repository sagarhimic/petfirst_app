from sqlalchemy import Column, Integer, String
from datetime import datetime, date
from sqlalchemy.orm import relationship
from app.core.database import Base

class NotificationType(Base):
    
    __tablename__ = "notification_types"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))

    notifications = relationship(
        "Notification",
        back_populates="type"
    )