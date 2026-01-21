from fastapi import APIRouter
from app.controllers.customers.booking_controller import get_bookings

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Bookings"]
)

router.post("/get-bookings")(get_bookings)