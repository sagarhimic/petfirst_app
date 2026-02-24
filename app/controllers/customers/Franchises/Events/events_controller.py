from fastapi import APIRouter, Depends, Query, Request, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.Events.events_service import get_events_list_service
from app.services.customers.Events.events_detail_service import get_event_details_service
from app.services.customers.Events.events_booking_service import create_event_booking_service

def get_events_list(
    request: Request,
    page: int = Query(1, ge=1),
    search_key: str | None = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_events_list_service(
        db=db,
        request=request,
        user_id=user_id,
        page=page,
        search_key=search_key
    )

# Event Details Showing

def show_event(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_event_details_service(
        db=db,
        request=request,
        event_id=event_id,
        user_id=user_id
    )

# Create Event Booking

async def create_event_booking(
    event_id: int,
    transaction_id: str = Form(...),
    payment_method: int = Form(...),
    payment_status: str = Form(...),
    pet_id: int = Form(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    data = {
        "transaction_id": transaction_id,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "pet_id": pet_id
    }

    return create_event_booking_service(
        db=db,
        event_id=event_id,
        user_id=user_id,
        data=data
    )
