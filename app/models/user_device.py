from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    device_type = Column(String(64))
    device_id = Column(String(128), index=True)
    device_model = Column(String(128))
    device_software = Column(String(128))
    device_manufacturer = Column(String(128))
    brand = Column(String(64))
    fcm_token = Column(String(255))
    app_version = Column(String(32))

    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
