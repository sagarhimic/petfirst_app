from fastapi import APIRouter
from app.controllers.customers.Franchises.Grooming.grooming_controller import get_grooming, grooming_details, create_grooming_booking, reschedule_grooming_booking, remove_grooming_service

router = APIRouter(
    prefix="/api/customer",
    tags=["Get Franchises/Grooming"]
)

router.get("/get-grooming-franchises")(get_grooming)
router.get("/get-grooming-details/{franchise_id}")(grooming_details)
router.post("/grooming-booking/{franchise_id}")(create_grooming_booking)
router.post("/reschedule-grooming-booking/{booking_id}")(reschedule_grooming_booking)
router.post("/remove-grooming-service/{service_id}")(remove_grooming_service)

