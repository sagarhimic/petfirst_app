from fastapi import APIRouter
from app.controllers.customers.reunion_controller import get_pet_parent, add_pet_parent, edit_pet_parent, update_pet_parent, delete_pet_parent  

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Reunion"]
)

router.get("/get-pet-parent")(get_pet_parent)
router.post("/add-pet-parent")(add_pet_parent)
router.get("/edit-pet-parent/{pet_parent_id}")(edit_pet_parent)
router.post("/update-pet-parent/{pet_parent_id}")(update_pet_parent)
router.post("/delete-pet-parent/{pet_parent_id}")(delete_pet_parent)
