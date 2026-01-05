from fastapi import APIRouter
from app.controllers.customers.auth_controller import sendOTP, validateOTP

router = APIRouter(prefix="/api/customers/login", tags=["Customer Auth"])

router.post("/auth/send-otp")(sendOTP)
router.post("/auth/validate-otp")(validateOTP)
