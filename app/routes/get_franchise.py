from fastapi import APIRouter
from app.controllers.customers.Franchises.Clinics.franchise_controller import get_franchises
from app.controllers.customers.Franchises.Clinics.doctor_controller import get_doctors, doctor_details

router = APIRouter(
    prefix="/api/customer",
    tags=["Get Franchises/Doctors"]
)

router.get("/get-franchises")(get_franchises)
router.get("/get-clinic-franchises/{franchise_id}")(get_doctors)
router.get("/get-doctor/{doctor_id}")(doctor_details)
