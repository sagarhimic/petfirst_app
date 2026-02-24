from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.bookings import Bookings
from app.models.booking_details import BookingDetails
from app.models.booking_trans import BookingTransaction
from app.utils.helpers import format_date


def booking_details_service(
    db: Session,
    user_id: int,
    booking_id: str
):
    try:
        # -----------------------------
        # Main booking
        # -----------------------------
        results = (
            db.query(Bookings)
            .filter(Bookings.booking_id == booking_id)
            .all()
        )

        if not results:
            return {
                "status": False,
                "message": "Booking not found"
            }

        # -----------------------------
        # Booking details
        # -----------------------------
        booking_details_raw = (
            db.query(BookingDetails)
            .filter(BookingDetails.booking_id == booking_id)
            .all()
        )

        bill_details_raw = (
            db.query(BookingTransaction)
            .filter(BookingTransaction.booking_id == booking_id)
            .first()
        )

        booking_details = []
        total_amount = 0

        for res in booking_details_raw:
            booking_details.append({
                "service_id": res.service.id if res.service else None,
                "service_name": res.service.service_name if res.service else None,
                "booking_from": format_date(res.booking_from) if res.booking_from else None,
                "booking_to": format_date(res.booking_to) if res.booking_to else None,
                "booking_time": res.booking_time.strftime("%I:%M %p") if res.booking_time else None,
                "amount": res.amount
            })
            total_amount += res.amount or 0

        # -----------------------------
        # Taxes
        # -----------------------------
        cgst = sgst = service_tax = 0
        cgst_comm = total_amount * cgst / 100
        sgst_comm = total_amount * sgst / 100
        service_tax_comm = total_amount * service_tax / 100
        total_service_taxes = cgst_comm + sgst_comm + service_tax_comm

        bill_details = {
            "transaction_id": bill_details_raw.transaction_id if bill_details_raw else None,
            "txn_amount": f"{bill_details_raw.txn_amount:,.2f}" if bill_details_raw else None,
            "payment_method": (
                "Online" if bill_details_raw and bill_details_raw.payment_method == 1
                else "Offline" if bill_details_raw and bill_details_raw.payment_method == 2
                else None
            ),
            "payment_date": format_date(bill_details_raw.payment_date) if bill_details_raw else None,
            "payment_status": bill_details_raw.tranStatus.name if bill_details_raw and bill_details_raw.tranStatus else None,
            "sub_total": total_amount,
            "cgst": cgst_comm,
            "sgst": sgst_comm,
            "service_tax": service_tax_comm,
            "service_fee_taxes": total_service_taxes,
            "total_amount": total_amount + total_service_taxes
        }

        # -----------------------------
        # Booking summary
        # -----------------------------
        bookings = []

        for r in results:
            name = event_date = event_time = doctor_note = booking_type = ""

            if r.service_type == 7 and r.bookingDetail and r.bookingDetail.eventname:
                ev = r.bookingDetail.eventname
                event_date = format_date(ev.event_date)
                event_time = f"{ev.event_time_from.strftime('%I:%M %p')} - {ev.event_time_to.strftime('%I:%M %p')}"
                name = ev.name

            elif r.service_type == 2:
                name = r.trainer.name if r.trainer else None

            elif r.service_type == 5:
                name = r.doctor.full_name if r.doctor else None
                booking_type = "Tele Medicine" if r.booking_type == 1 else "House Call"

            bookings.append({
                "booking_id": r.booking_id,
                "booking_type": booking_type,
                "booking_date": format_date(r.booking_date),
                "franchise_id": r.franchise_id,
                "doctor_id": r.doctor_id,
                "franchise_name": "Pet-First",
                "franchise": r.franchise.location if r.franchise else None,
                "franchise_pincode": r.franchise.pin_code if r.franchise else None,
                "franchise_mobile": r.franchise.contact_number if r.franchise else None,
                "service_type": r.servicetype.service_name if r.servicetype else None,
                "event_date": event_date,
                "event_time": event_time,
                "trainer_id": r.trainer_id,
                "name": name,
                "total_amount": r.total_amount,
                "gst": r.gst,
                "sgst": r.sgst,
                "discount": r.discount,
                "booking_status": r.bookingstatus.name if r.bookingstatus else None,
                "booking_sub_status": "Rescheduled" if r.sub_status_id == 1 else None,
                "booking_created": format_date(r.created_at),
                "booking_details": booking_details if booking_details else None,
                "transaction_details": bill_details if bill_details else None,
                "doctor_note": doctor_note
            })

        return {
            "status": True,
            "data": bookings,
            "message": "Bookings Details Info."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
