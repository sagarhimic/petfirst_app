from sqlalchemy.orm import Session
from app.models.user_device import UserDevice
from datetime import datetime

def save_device_details(db: Session, data, user_id: int):
    # Skip if device_id missing (web login)
    if not data.device_id:
        return True

    device = (
        db.query(UserDevice)
        .filter(
            UserDevice.user_id == user_id,
            UserDevice.device_id == data.device_id
        )
        .first()
    )

    if device:
        # update
        device.device_type = data.device_type
        device.device_model = data.device_model
        device.device_software = data.device_software
        device.device_manufacturer = data.device_manufacturer
        device.brand = data.brand
        device.fcm_token = data.fcm_token
        device.app_version = data.app_version
        device.status = 1
    else:
        # insert
        device = UserDevice(
            user_id=user_id,
            device_type=data.device_type,
            device_id=data.device_id,
            device_model=data.device_model,
            device_software=data.device_software,
            device_manufacturer=data.device_manufacturer,
            brand=data.brand,
            fcm_token=data.fcm_token,
            app_version=data.app_version,
            status=1,
            created_at=datetime.utcnow()
        )
        db.add(device)

    db.commit()
    return True
