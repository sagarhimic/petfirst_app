from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class TransactionStatus(Base):
    __tablename__ = "transaction_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    status_id = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

