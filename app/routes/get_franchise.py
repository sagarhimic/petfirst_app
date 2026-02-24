from fastapi import APIRouter
from app.controllers.customers.Franchises.Clinics.franchise_controller import get_franchises
from app.controllers.customers.Franchises.Clinics.doctor_controller import get_doctors, doctor_details, create_doctor_booking, reschedule_clinic_booking, generate_time_slots

router = APIRouter(
    prefix="/api/customer",
    tags=["Get Franchises/Doctors"]
)

router.get("/get-franchises")(get_franchises)
router.get("/get-clinic-franchises/{franchise_id}")(get_doctors)
router.get("/get-doctor/{doctor_id}")(doctor_details)
router.post("/clinic-booking/{doctor_id}")(create_doctor_booking)
router.post("/reshedule/clinic-booking/{booking_id}")(reschedule_clinic_booking)
router.get("/get-clinic-timeslots")(generate_time_slots)
