from fastapi import APIRouter
from app.controllers.customers.Franchises.Grooming.grooming_controller import get_grooming, grooming_details

router = APIRouter(
    prefix="/api/customer",
    tags=["Get Franchises/Grooming"]
)

router.get("/get-grooming-franchises")(get_grooming)
router.get("/get-grooming-details/{franchise_id}")(grooming_details)

