from fastapi import APIRouter
from app.controllers.customers.cart_controller import add_to_cart, cart_details, remove_service, clear_cart

router = APIRouter(prefix="/api/customer",
    tags=["Customer Cart"])

router.post("/add-to-cart")(add_to_cart)
router.get("/get-cart-details")(cart_details)
router.post("/remove-service-to-cart/{service_id}")(remove_service)
router.get("/clear-cart/{trainer_id}")(clear_cart)
