from fastapi import APIRouter
from app.controllers.customers.pet_adoption_controller import add_enquiry, enquiries_list, get_online_pets_list, pet_adoption_details

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer pet adoption"]
)

router.post("/create-enquiry/{pet_adoption_id}")(add_enquiry)
router.get("/enquiries-list")(enquiries_list)
router.post("/get-online-pets-list")(get_online_pets_list)
router.get("/pet-adoption-details/{pet_id}")(pet_adoption_details)






