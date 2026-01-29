from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class BookingTransaction(Base):
    
    __tablename__ = "booking_transactions"
    
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer)
    phonepe_reference_no = Column(String(255))
    transaction_id = Column(String(255))
    txn_amount = Column(Numeric(10, 2), nullable=True)
    payment_method = Column(Integer)
    payment_mode = Column(String(45))
    payment_date = Column(DateTime, nullable=True)
    payment_status = Column(Integer)
    payment_json_raw = Column(Text)
    payment_bank = Column(String(15))
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)


    tranStatus = relationship(
        "TransactionStatus",
        primaryjoin="BookingTransaction.payment_status == foreign(TransactionStatus.id)",
        uselist=False,
        viewonly=True
    )