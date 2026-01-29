from fastapi import APIRouter
from app.controllers.customers.booking_controller import get_bookings, cancel_booking
from app.controllers.customers.booking_details_controller import get_booking_details

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Bookings"]
)

router.post("/get-bookings")(get_bookings)
router.get("/get-booking-details/{booking_id}")(get_booking_details)
router.post("/cancel-booking")(cancel_booking)