from fastapi import APIRouter
from app.controllers.customers.bank_controller import get_bank_details, add_bank_details, update_bank_primary, delete_bank_account

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Bank Info"]
)

router.get("/get-bank-details")(get_bank_details)
router.post("/add-bank-details")(add_bank_details)
router.post("/update-bank-primary/{bank_id}")(update_bank_primary)
router.post("/delete-bank-account/{bank_id}")(delete_bank_account)
