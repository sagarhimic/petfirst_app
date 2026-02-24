# app/models/trainers/assign_trainer_service.py
from sqlalchemy import Column, Integer, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class UserService(Base):
    __tablename__ = "assign_trainer_services"

    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))   # ✅ FIXED
    service_id = Column(Integer, ForeignKey("sub_services.id"))  # ✅ FIXED

    duration = Column(Text)
    price = Column(Numeric(10, 2), nullable=True)
    status = Column(Integer)
    approved_by = Column(Integer)
    approve_status = Column(Integer)
    approved_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer)

    # ✅ STRING reference is OK *only if class exists*
    subservice = relationship(
        "SubService",
        back_populates="assign_trainer_services"
    )

    # trainer_cart_details = relationship(
    #     "TrainerCartDetails",
    #     primaryjoin="UserService.service_id == foreign(TrainerCartDetails.service_id)",
    #     viewonly=True
    # )