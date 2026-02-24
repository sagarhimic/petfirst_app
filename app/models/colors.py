from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship


class Colors(Base):
    __tablename__ = "pet_colors"

    id = Column(Integer, primary_key=True, index=True)
    pet_type_id = Column(Integer)
    name = Column(String(55), nullable=True)

    # Relationship back to OnlinePets
    online_pets = relationship("OnlinePets", back_populates="color_name")

  
 