from fastapi import Depends, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.trainer_booking_service import create_booking_service


def create_booking(
    total_amount: float = Form(...),
    discount: float = Form(0),
    gst: float = Form(None),
    sgst: float = Form(None),
    service_tax: float = Form(None),
    payment_method: int = Form(...),
    payment_status: str = Form(...),
    transaction_id: str = Form(...),
    
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):

    data = {
        "total_amount": total_amount,
        "discount": discount,
        "gst": gst,
        "sgst": sgst,
        "service_tax": service_tax,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "transaction_id": transaction_id
    }
    
    return create_booking_service(
        db=db,
        user_id=user_id,
        data=data
    )
