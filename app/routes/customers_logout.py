from fastapi import APIRouter
from app.controllers.customers.logout_controller import logout

router = APIRouter(
    prefix="/api/customers", 
    tags=["Customer Auth"]
)

router.post("/customer/logout")(logout)
