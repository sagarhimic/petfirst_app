from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Numeric, DateTime, Time
from sqlalchemy.orm import relationship, foreign
from datetime import datetime, time
from app.core.database import Base

class Bookings(Base):
    
    __tablename__ = "bookings"
    
    booking_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("franchises.id"))
    service_type = Column(Integer, ForeignKey("services.id"))
    booking_type = Column(Integer)
    booking_date = Column(DateTime, nullable=True)
    booking_to = Column(DateTime, nullable=True)
    booking_time = Column(Time, nullable=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    pet_id = Column(Integer, ForeignKey("pet_info.id"))
    doctor_id = Column(Integer, ForeignKey("franchise_users.id"))
    total_amount = Column(Numeric(10, 2), nullable=True)
    discount = Column(Numeric(10, 2), nullable=True)
    gst= Column(Numeric(10, 2), nullable=True)
    sgst= Column(Numeric(10, 2), nullable=True)
    service_tax  = Column(Numeric(10, 2), nullable=True)
    booking_status = Column(Integer, ForeignKey("booking_statuses.id"))
    sub_status_id = Column(Integer)
    cancel_reason = Column(Integer)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)


    # Relationships Used for Bookings Model

    trainer = relationship("Trainer", back_populates="bookings")

    franchise = relationship("Franchise", back_populates="bookings")

    customer = relationship("User", back_populates="bookings")

    customer_location = relationship(
        "BookingAddress",
        primaryjoin="Bookings.booking_id == BookingAddress.booking_id",
        uselist=False
    )

    # 🔹 doctor (FranchiseUsers)
    doctor = relationship(
        "Doctor",
        foreign_keys=[doctor_id],
        back_populates="bookings"
    )

    # 🔹 doctor detail (DoctorInfo)
    doctor_detail = relationship(
        "DoctorInfo",
        primaryjoin="Bookings.doctor_id == DoctorInfo.doctor_id",
        foreign_keys="DoctorInfo.doctor_id",
        uselist=False,
        viewonly=True
    )

    pet = relationship("PetInfo", back_populates="bookings")

    servicetype = relationship("Services", back_populates="bookings")

    bookingstatus = relationship("BookingStatus", back_populates="bookings")

    booking_detail = relationship(
        "BookingDetails",
        primaryjoin="Bookings.booking_id == BookingDetails.booking_id",
        uselist=False
    )

    booking_trans = relationship(
    "BookingTransaction",
    primaryjoin="Bookings.booking_id == foreign(BookingTransaction.booking_id)",
    uselist=False,
    viewonly=True
)

