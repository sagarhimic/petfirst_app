
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Enquiry(Base):
    __tablename__ = "enquiries"
    __table_args__ = {'extend_existing': True}

    enquiry_id = Column(Integer, primary_key=True, index=True)

    service_type = Column(Integer,  nullable=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    franchise_id = Column(Integer,  nullable=True)

    enquiry_date = Column(DateTime, nullable=True)
    status_id = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)
    contact_method = Column(String, nullable=True)
    time_to_contact = Column(String, nullable=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
  #  franchise = relationship("Franchise", back_populates="enquiries", foreign_keys=[franchise_id])
    enquiry_details = relationship("EnquiryDetail", back_populates="enquiry", primaryjoin="Enquiry.enquiry_id==EnquiryDetail.enquiry_id")
 #   service_type_rel = relationship("Services", back_populates="enquiries", foreign_keys=[service_type])
    customer = relationship("User", foreign_keys=[customer_id])
    seller = relationship("User", foreign_keys=[seller_id])
    createdby = relationship("User", foreign_keys=[created_by])
    updatedby = relationship("User", foreign_keys=[updated_by])