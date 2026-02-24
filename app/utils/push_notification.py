# app/utils/push_notification.py

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user_device import UserDevice
from app.models.trainer_device import TrainerDevice
from app.services.push_service import PushNotificationService


def push_notification(db: Session, users: list, send_data: dict, user_type="user"):

    if not users:
        return False

    # Fetch Devices
    if user_type == "trainer":
        devices = db.query(TrainerDevice).filter(
            TrainerDevice.user_id.in_(users),
            TrainerDevice.fcm_token != None,
            TrainerDevice.fcm_token != ""
        ).all()
    else:
        devices = db.query(UserDevice).filter(
            UserDevice.user_id.in_(users),
            UserDevice.fcm_token != None,
            UserDevice.fcm_token != ""
        ).all()

    for device in devices:

        PushNotificationService.send_push(
            token=device.fcm_token,
            title=send_data.get("title"),
            message=send_data.get("desc", send_data.get("title"))
        )

    return True