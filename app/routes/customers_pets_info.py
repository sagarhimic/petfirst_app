from fastapi import APIRouter
from app.controllers.customers.pet_controller import store_pet, update_pet_pic, get_pet_details, update_pet, pet_update_primary, edit_pet_details

router = APIRouter(prefix="/api/customer", tags=["Customer Add Pet Info"])

router.post("/add-pet")(store_pet)
router.post("/update-pet-pic/{pet_id}")(update_pet_pic)
router.get("/get-pet-details")(get_pet_details)
router.post("/update-pet/{pet_id}")(update_pet)
router.post("/add-primary-pet")(pet_update_primary)
router.get("/get-pet/{pet_id}")(edit_pet_details)
