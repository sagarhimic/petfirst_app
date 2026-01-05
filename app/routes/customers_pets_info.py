from fastapi import APIRouter
from app.controllers.customers.pet_controller import store_pet_details

router = APIRouter(prefix="/api/customer/add-pet", tags=["Customer Add Pet Info"])

router.post("/customer/add-pet")(store_pet_details)
