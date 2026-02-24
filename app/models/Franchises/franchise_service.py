from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class FranchiseService(Base):
    __tablename__ = "franchise_services"

    id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer)
    service_type = Column(Integer)
    service_id = Column(
        Integer,
        ForeignKey("sub_services.id")  # ✅ VERY IMPORTANT
    )
    status_id = Column(Integer)

    # ✅ Laravel belongsTo equivalent
    subservice = relationship(
        "SubService",
        back_populates="franchise_services"
    )
    

