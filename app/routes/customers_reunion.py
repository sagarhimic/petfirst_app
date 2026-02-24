from fastapi import APIRouter
from app.controllers.customers.reunion_controller import get_pet_parent, add_pet_parent, edit_pet_parent, update_pet_parent, delete_pet_parent  

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Reunion"]
)

router.get("/get-pet-parent")(get_pet_parent)
router.post("/add-pet-parent")(add_pet_parent)
router.get("/pet-parent/{pet_parent_id}")(edit_pet_parent)
router.post("/pet-parent/{pet_parent_id}/update")(update_pet_parent)
router.post("/pet-parent-delete/{pet_parent_id}")(delete_pet_parent)
