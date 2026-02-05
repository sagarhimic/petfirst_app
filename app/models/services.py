from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base

class Services(Base):
    
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True)
    service_name = Column(String(125))
    image = Column(Text)
    status_id = Column(Integer)
    order = Column(Integer)

    bookings = relationship(
        "Bookings",
        foreign_keys="Bookings.service_type",
        back_populates="servicetype"
    )

    # trainer_carts = relationship("TrainerCart", back_populates="servicename")