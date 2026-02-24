from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class OnlinePetImages(Base):
    __tablename__ = "online_pet_images"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("online_pets.product_id"),
        nullable=False
    )

    pet_pic = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 🔗 Relationships 
    online_pet = relationship(
        "OnlinePets",
        back_populates="petImages",
        foreign_keys=[product_id]
    )
    
    createdby = relationship(
        "User",
        foreign_keys=[created_by],
        lazy="joined"
    )

    updatedby = relationship(
        "User",
        foreign_keys=[updated_by],
        lazy="joined"
    )