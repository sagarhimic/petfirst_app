from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_trans import BookingTransaction
from app.utils.helpers import get_order_date_format


def create_bill_service(
    db: Session,
    booking_id: int,
    data: dict
):
    try:
        booking = (
            db.query(Bookings)
            .filter(Bookings.booking_id == booking_id)
            .first()
        )

        if not booking:
            return {
                "status": False,
                "message": "Booking ID not found.",
                "bill_details": []
            }

        booking_details = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_id == booking_id)
            .all()
        )

        if data.get("payment_status") != "success":
            return {
                "status": False,
                "message": "Payment transaction failed. Booking not created.",
                "bill_details": []
            }

        # -----------------------------
        # Create transaction
        # -----------------------------
        bill = BookingTransaction(
            booking_id=booking_id,
            transaction_id=data.get("transaction_id"),
            txn_amount=data.get("total_amount"),
            payment_method=data.get("payment_method"),
            payment_date=datetime.utcnow(),
            payment_status=6,
            created_at=datetime.utcnow()
        )

        # print(f"Response: {bill}")

        db.add(bill)
        db.flush()  # get bill.id

        # -----------------------------
        # Service details
        # -----------------------------
        service_details = []
        sub_total = 0

        for detail in booking_details:
            if detail.service_id:
                name = detail.service.service_name if detail.service else None
            elif detail.event_id:
                name = detail.eventname.name if detail.eventname else None
            elif detail.doctor_id:
                name = detail.doctor.full_name if detail.doctor else None
            else:
                name = None

            service_details.append({
                "name": name,
                "booking_date": get_order_date_format(detail.booking_from),
                "booking_time": detail.booking_time,
                "amount": detail.amount
            })

            sub_total += detail.amount or 0

        bill_details = {
            "sub_total": sub_total,
            "taxes": (booking.gst or 0) + (booking.sgst or 0) + (booking.service_tax or 0),
            "total_amount": booking.total_amount
        }

        # -----------------------------
        # Update booking status
        # -----------------------------
        booking.booking_status = 1
        db.commit()

        return {
            "status": True,
            "message": "Booking and bill created successfully.",
            "bill": {
                "id": bill.id,
                "transaction_id": bill.transaction_id,
                "txn_amount": float(bill.txn_amount),
                "payment_method": bill.payment_method,
                "payment_date": bill.payment_date
            },
            "service_details": service_details,
            "bill_details": bill_details
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )
