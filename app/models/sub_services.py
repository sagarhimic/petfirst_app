from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class SubService(Base):
    
    __tablename__ = "sub_services"
    
    id = Column(Integer, primary_key=True)
    service_type = Column(Integer, ForeignKey("trainers.id"))
    package_type = Column(Integer)
    service_name = Column(String(125))
    description = Column(Text)
    duration = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    image = Column(Text, nullable=True)
    status_id = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    # 🔁 reverse relationship (MANDATORY)
    assign_trainer_services = relationship(
        "UserService",
        back_populates="subservice"
    )

    # 🔁 hasMany(SubCategoryServices)
    sub_category_services = relationship(
        "SubCategoryServices",
        back_populates="category"
    )

    franchise_services = relationship(
        "FranchiseService",
        back_populates="subservice"
    )

    cartserv = relationship(
        "GroomingCartDetails",
        back_populates="servicetemp"
    )

    trainer_service_reviews = relationship(
        "TrainerServiceReview",
        back_populates="service"
    )