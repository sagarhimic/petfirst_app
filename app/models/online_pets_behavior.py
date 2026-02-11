from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class OnlinePetsBehavior(Base):
    __tablename__ = "online_pets_behavior"

    id = Column(Integer, primary_key=True, index=True)
    online_pet_id = Column(Integer, ForeignKey("online_pets.product_id"), nullable=False)
    behavior_id = Column(Integer, ForeignKey("pet_behaviors.id"), nullable=False)

    # 🔗 Relationship (belongsTo PetBehavior)
   # behavior = relationship("PetBehavior", back_populates="online_pet_behaviors")