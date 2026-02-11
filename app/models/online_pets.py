from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, Float
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class OnlinePets(Base):
    __tablename__ = "online_pets"
    __table_args__ = {"extend_existing": True}

    # Primary Key
    product_id = Column(Integer, primary_key=True, index=True)

    # Columns
    owner_id = Column(Integer, ForeignKey("users.id"))
    pet_name = Column(String)
    age = Column(Integer)
    dob = Column(DateTime)

    breed = Column(Integer, ForeignKey("breeds.id"))
    color = Column(Integer, ForeignKey("pet_colors.id"))

    height = Column(String)
    weight = Column(String)

    status = Column(Integer)
    price = Column(Float)
    discount = Column(Float)
    quantity = Column(Integer)

    gender = Column(Integer, ForeignKey("gender_types.id"))
    description = Column(String)

    pet_type = Column(Integer, ForeignKey("pet_types.id"))
    size = Column(String)
    vaccine = Column(String)

    pet_story = Column(String)
    personality = Column(String)
    health = Column(String)
    compatibility = Column(String)

    life_span_from = Column(Integer)
    life_span_to = Column(Integer)

    delivery_type = Column(String)

    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("users.id"))

    # -------------------
    # Relationships (Laravel equivalent)
    # -------------------

    # belongsTo PetBreeds
    breed_name = relationship(
        "Breeds",
        back_populates="online_pets",
        foreign_keys=[breed]
    )

    # belongsTo PetColors
    color_name = relationship("Colors", back_populates="online_pets", foreign_keys=[color]) 

    # belongsTo User
    owner = relationship(
        "User",
        foreign_keys=[owner_id]
    )

    createdby = relationship(
        "User",
        foreign_keys=[created_by]
    )

    updatedby = relationship(
        "User",
        foreign_keys=[updated_by]
    )

    # belongsTo Gender
    genderinfo = relationship(
        "GenderInfo",
        foreign_keys=[gender]
    )

    # hasMany OnlinePetImages
    petImages = relationship("OnlinePetImages", back_populates="online_pet")

    # belongsTo Pettype
    pettype = relationship(
        "PetTypes",
        foreign_keys=[pet_type]
    )