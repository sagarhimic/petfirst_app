from fastapi import APIRouter
from app.controllers.customers.pet_controller import store_pet

router = APIRouter(prefix="/api/customer", tags=["Customer Add Pet Info"])

router.post("/add-pet")(store_pet)
