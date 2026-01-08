from fastapi import APIRouter
from app.controllers.customers.trainer_controller import get_trainers

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Get Trainers"]
)

router.get("/get-trainers")(get_trainers)
