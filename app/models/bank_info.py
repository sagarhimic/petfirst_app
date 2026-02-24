
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.database import Base

class CustomerBankDetails(Base):
    __tablename__ = "customer_bank_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    bank_name = Column(String(255), nullable=True)
    account_holder_name = Column(String(255), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc = Column(String(50), nullable=True)
    recipient_id = Column(String(255), nullable=True)

    is_primary = Column(Boolean, default=False)
    status_id = Column(Integer, default=1)

    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship (belongsTo in Laravel)
   # user = relationship("User", back_populates="bank_accounts")