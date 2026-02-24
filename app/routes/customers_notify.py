from fastapi import APIRouter
from app.controllers.customers.Notifications.notification_controller import get_notifications, clear_notifications

router = APIRouter(prefix="/api/customer",  tags=["Customer Notifications"])

router.get("/get-notify")(get_notifications)
router.get("/clear-notify")(clear_notifications)
