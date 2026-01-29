from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, date
from app.core.database import Base

class Notification(Base):
    
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    title = Column(String(255))
    link = Column(String(255))
    customer_id = Column(Integer)
    seller_id = Column(Integer)
    trainer_id = Column(Integer)
    franchise_user_id = Column(Integer)
    booking_id = Column(Integer)
    order_id = Column(Integer)
    franchise_id = Column(Integer)
    enquiry_id = Column(Integer)
    status_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)