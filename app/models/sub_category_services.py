from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class SubCategoryServices(Base):
    
    __tablename__ = "sub_category_services"

    id = Column(Integer, primary_key=True)
    sub_service_id = Column(Integer)
    service_id = Column(Integer, ForeignKey("sub_services.id"))  # ✅ FK

    category = relationship(
        "SubService",
        back_populates="sub_category_services"
    )
