
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("notification_types.id"), nullable=False)

    title = Column(String(255), nullable=True)
    link = Column(String(255), nullable=True)

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    seller_id = Column(Integer, nullable=True)
    trainer_id = Column(Integer, nullable=True)
    franchise_user_id = Column(Integer, nullable=True)

    booking_id = Column(BigInteger, nullable=True)
    order_id = Column(Integer, nullable=True)
    franchise_id = Column(Integer, nullable=True)
    enquiry_id = Column(Integer, nullable=True)

    status_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # -------------------------
    # Relationships
    # -------------------------
    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="notifications"
    )

    notification_users = relationship(
        "NotificationUser",
        back_populates="notification",
        cascade="all, delete-orphan"
    )

    type = relationship(
        "NotificationType",
        back_populates="notifications"
    )
