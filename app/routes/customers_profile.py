from fastapi import APIRouter
from app.controllers.customers.profile_controller import get_profile

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Profile"]
)

router.get("/get-profile")(get_profile)
