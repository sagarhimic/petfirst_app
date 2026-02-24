# app/models/notifications/notification_user.py

from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class NotificationUser(Base):
    __tablename__ = "notification_users"

    noti_id = Column(
        BigInteger,
        ForeignKey("notifications.id", ondelete="CASCADE"),
        primary_key=True
    )

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    seller_id = Column(Integer, nullable=True)
    trainer_id = Column(Integer, nullable=True)
    franchise_id = Column(Integer, nullable=True)
    franchise_user_id = Column(Integer, nullable=True)

    status = Column(Integer, default=1)  # 1 = Unread, 2 = Read
    management_status = Column(Integer, nullable=True)

    # -------------------------
    # Relationships
    # -------------------------
    notification = relationship(
        "Notification",
        back_populates="notification_users"
    )

    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="notification_users"
    )
