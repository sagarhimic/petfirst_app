
from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base


class SMSLog(Base):
    __tablename__ = "sms_logs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    receiver_name = Column(String(255), nullable=False)
    receiver_mobile = Column(Text, nullable=False)

    user_id = Column(BigInteger, nullable=True)

    purpose = Column(String(128), nullable=False)

    message = Column(Text, nullable=False)

    sender_id = Column(BigInteger, nullable=True)
    sender_name = Column(String(255), nullable=True)

    response_id = Column(String(32), nullable=False)
    status = Column(String(255), nullable=False)

    count = Column(Integer, nullable=False)
    sms_count = Column(Integer, nullable=True)

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False
    )

    vendor = Column(BigInteger, nullable=True)
    sms_type = Column(BigInteger, nullable=True)