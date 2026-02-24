from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.Franchises.Events.events import Event
from app.models.Franchises.Events.event_gallery import EventGallery
from app.models.Franchises.Events.event_benefits import EventBenefit
from app.utils.helpers import build_full_url, format_date, format_time
from app.utils.tax import total_price


def get_event_details_service(
    db: Session,
    request: Request,
    event_id: int,
    user_id: int
):
    try:
        # -----------------------------------
        # Fetch event
        # -----------------------------------
        event = (
            db.query(Event)
            .filter(Event.id == event_id)
            .first()
        )

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # -----------------------------------
        # Gallery & Benefits
        # -----------------------------------
        gallery = (
            db.query(EventGallery)
            .filter(EventGallery.event_id == event_id)
            .all()
        )

        benefits = (
            db.query(EventBenefit)
            .filter(EventBenefit.event_id == event_id)
            .all()
        )

        # -----------------------------------
        # Tax Calculation (Laravel equivalent)
        # -----------------------------------
        entry_fee = float(event.entry_fee or 0)

        CGST = 9
        SGST = 9
        SERVICE_TAX = 5

        calc = total_price(
            entry_fee,
            CGST,
            SGST,
            SERVICE_TAX
        )

        total_service_tax = (
            calc["cgst_fee"]
            + calc["sgst_fee"]
            + calc["service_tax"]
        )

        fee_details = {
            "entry_fee": int(entry_fee),
            "cgst": calc["cgst_fee"],
            "sgst": calc["sgst_fee"],
            "service_tax": calc["service_tax"],
            "service_tax_fee": total_service_tax,
            "total_amount": calc["total_amount"]
        }

        # -----------------------------------
        # Response mapping
        # -----------------------------------
        event_data = {
            "event_id": event.id,
            "name": event.name,
            "about": event.about,
            "event_date": format_date(event.event_date),
            "event_time_from": format_time(event.event_time_from),
            "event_time_to": format_time(event.event_time_to),
            "location": event.location,
            "city": event.city,
            "state_id": event.state_id,
            "state": event.state.name if event.state else None,
            "country_id": event.country_id,
            "country": event.country.name if event.country else None,
            "pincode": event.pincode,
            "entry_fee": event.entry_fee,
            "discount": event.discount,
            "status_id": 1,
            "gallery": [
                {
                    "image": build_full_url(request, g.image)
                }
                for g in gallery
            ] if gallery else None,
            "benefits": [
                {
                    "benefit_name": b.benefit_name
                }
                for b in benefits
            ] if benefits else None
        }

        return {
            "status": True,
            "data": event_data,
            "payment_details": fee_details
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
