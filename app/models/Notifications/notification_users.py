from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, date
from app.core.database import Base

class NotificationUser(Base):
    
    __tablename__ = "notification_users"
    
    noti_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    seller_id = Column(Integer)
    trainer_id = Column(Integer)
    franchise_id = Column(Integer)
    franchise_user_id = Column(Integer)
    status = Column(Integer)
    management_status = Column(Integer)