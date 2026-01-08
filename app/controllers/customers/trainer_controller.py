from fastapi import Depends, Request, Form, Query
from decimal import Decimal
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.customers.trainer_schema import GetTrainersRequest
from app.services.customers.trainer_service import get_trainers_service

def get_trainers(
    latitude: Decimal = Query(...),
    longitude: Decimal = Query(...),
    service_id: Optional[int] = Query(None),
    trainer_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    data = GetTrainersRequest(
        latitude=latitude,
        longitude=longitude,
        service_id=service_id,
        trainer_id=trainer_id
    )

    trainers = get_trainers_service(db, data)

    return {
        "status": True,
        "message": "Trainers Info.",
        "data": trainers
    }