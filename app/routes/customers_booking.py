from fastapi import APIRouter
from app.controllers.customers.booking_controller import get_bookings, cancel_booking
from app.controllers.customers.booking_details_controller import get_booking_details
from app.controllers.customers.upcoming_bookings_controller import upcoming_bookings
from app.controllers.customers.trainer_bookings_controller import create_booking, reschedule_booking

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Bookings"]
)

router.post("/get-bookings")(get_bookings)
router.get("/get-booking-details/{booking_id}")(get_booking_details)
router.post("/cancel-booking")(cancel_booking)
router.get("/get-upcoming-bookings")(upcoming_bookings)
router.post("/create-trainer-booking")(create_booking)
router.post("/reschedule-trainer-booking")(reschedule_booking)