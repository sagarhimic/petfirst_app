
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EnquiryDetail(Base):
    __tablename__ = "enquiry_details"
    __table_args__ = {"extend_existing": True}

    enquiry_detail_id = Column(Integer, primary_key=True, index=True)

    enquiry_id = Column(Integer, ForeignKey("enquiries.enquiry_id"))
    product_id = Column(Integer, ForeignKey("online_pets.product_id"))

    # Relationships
    enquiry = relationship("Enquiry", back_populates="enquiry_details")
  #  product = relationship("OnlinePets", back_populates="pet_enquiries")