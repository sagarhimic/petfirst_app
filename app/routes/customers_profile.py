from fastapi import APIRouter
from app.controllers.customers.profile_controller import delete_location, get_profile, save_location, modify_profile_name, update_profile_pic, get_locations, update_primary_location

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Profile"]
)

router.get("/get-profile")(get_profile)
router.post("/add-user-location/{user_id}")(save_location)
router.post("/modify-profile-name")(modify_profile_name)
router.post("/update-profile-pic")(update_profile_pic)
router.get("/get-locations")(get_locations)
router.post("/add-primary-location")(update_primary_location)
router.post("/delete-location/{location_id}")(delete_location)
