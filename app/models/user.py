from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    mobile = Column(String(15), unique=True)
    email = Column(String(100))
    name = Column(String(150))
    status = Column(Integer, default=1)
    role_id = Column(Integer, default=2)
    login_type = Column(Integer)
    user_type_id = Column(Integer)
    logged_in = Column(Integer)
    user_token = Column(String(125))
    token_expiration = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)
    last_logged_in_at = Column(DateTime, default=datetime.utcnow)
    access_for = Column(Integer, nullable=True)

    bookings = relationship("Bookings",back_populates="customer")