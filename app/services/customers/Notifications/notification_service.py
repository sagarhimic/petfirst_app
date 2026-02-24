# app/services/notifications/notification_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_

from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from app.utils.helpers import build_full_url



def get_notification_service(
    db: Session,
    request,
    user_id: int
):
    try:
        # -----------------------------
        # Join notifications + notification_users
        # -----------------------------
        notifications = (
            db.query(Notification)
            .join(
                NotificationUser,
                Notification.id == NotificationUser.noti_id
            )
            .filter(
                NotificationUser.customer_id == user_id,
                NotificationUser.status == 1
            )
            .all()
        )

        notifications_count = len(notifications)

        notify = []

        for noti in notifications:
            notify.append({
                "noti_id": noti.id,
                "type_id": noti.type_id,
                "title": noti.type.name if noti.type else None,
                "description": noti.title,
                "link": noti.link,
                "id": noti.booking_id if noti.booking_id else noti.order_id
            })

        if notifications_count > 0:
            return {
                "status": True,
                "data": notify,
                "notification_count": notifications_count,
                "img": build_full_url(request, "uploads/default_notification.png"),
                "from": "Petfirst"
            }

        return {
            "status": True,
            "data": [],
            "notification_count": 0
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )


def clear_notification_service(db: Session, user_id: int):
    try:
        db.query(NotificationUser) \
            .filter(NotificationUser.customer_id == user_id) \
            .delete(synchronize_session=False)

        print(user_id)

        db.commit()

        return {
            "status": True,
            "message": "Notifications deleted successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))