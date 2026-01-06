from fastapi import APIRouter
from app.controllers.customers.pet_controller import store_pet, update_pet_pic

router = APIRouter(prefix="/api/customer", tags=["Customer Add Pet Info"])

router.post("/add-pet")(store_pet)
router.post("/update-pet-pic/{pet_id}")(update_pet_pic)
