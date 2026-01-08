from fastapi import APIRouter
from app.controllers.customers.profile_controller import get_profile, save_location

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Profile"]
)

router.get("/get-profile")(get_profile)
router.post("/add-user-location/{user_id}")(save_location)
