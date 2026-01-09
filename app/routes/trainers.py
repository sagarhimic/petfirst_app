from fastapi import APIRouter
from app.controllers.customers.trainer_controller import get_trainers, trainer_details

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Get Trainers"]
)

router.get("/get-trainers")(get_trainers)
router.get("/get-trainers-details/{trainer_id}")(trainer_details)
