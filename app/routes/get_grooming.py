from fastapi import APIRouter
from app.controllers.customers.Franchises.Grooming.grooming_controller import get_grooming, grooming_details, create_grooming_booking, reschedule_grooming_booking, remove_grooming_service
from app.controllers.customers.Franchises.Grooming.grooming_cart_controller import add_cart_grooming, get_cart_details, clear_cart_api, remove_service_by_cart_api, modify_service_by_cart_api
router = APIRouter(
    prefix="/api/customer",
    tags=["Get Franchises/Grooming"]
)

router.get("/get-grooming-franchises")(get_grooming)
router.get("/get-grooming-details/{franchise_id}")(grooming_details)
router.post("/grooming-booking/{franchise_id}")(create_grooming_booking)
router.post("/reschedule-grooming-booking/{booking_id}")(reschedule_grooming_booking)
router.post("/remove-grooming-service/{service_id}")(remove_grooming_service)

# Grooming Cart 

router.post("/add-cart-grooming")(add_cart_grooming)
router.get("/get-cart-grooming-details")(get_cart_details)
router.post("/clear-grooming-cart/{franchise_id}")(clear_cart_api)
router.post("/remove-grooming-service-to-cart/{cart_id}")(remove_service_by_cart_api)
router.post("/edit-cart-grooming/{cart_id}")(modify_service_by_cart_api)

