# app/controllers/customers/notification_controller.py

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.services.customers.Notifications.notification_service import get_notification_service, clear_notification_service

def get_notifications(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return get_notification_service(
        db=db,
        request=request,
        user_id=user_id
    )

def clear_notifications(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_auth_user_id)
):
    return clear_notification_service(
        db=db,
        user_id=user_id
    )