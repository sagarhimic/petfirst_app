from fastapi import APIRouter
from app.controllers.customers.cart_controller import add_to_cart, cart_details

router = APIRouter(prefix="/api/customer",
    tags=["Customer Cart"])

router.post("/add-to-cart")(add_to_cart)
router.get("/get-cart-details")(cart_details)
