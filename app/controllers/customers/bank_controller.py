from fastapi import Depends, Request, Form, UploadFile, File
from decimal import Decimal
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.jwt_auth import get_auth_user_id
from app.schemas.customers.auth_schema import ValidateUserLocationRequest
from app.services.customers.bank_service import add_bank_details_service, get_bank_details_service, update_bank_primary_service, delete_bank_account_service
from app.schemas.customers.bank_schema import StoreBankRequest, UpdateBankRequest


def get_bank_details(
    request: Request,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return get_bank_details_service(db, user_id, request)

def add_bank_details(
    bank_name: str = Form(...),
    account_holder_name: str = Form(...),
    account_number: str = Form(...),
    ifsc: str = Form(...),
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    data = StoreBankRequest(
        bank_name=bank_name,
        account_holder_name=account_holder_name,
        account_number=account_number,
        ifsc=ifsc
    )

    return add_bank_details_service(db, user_id, data)

def update_bank_primary(
    bank_id: int,   
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):   
    return update_bank_primary_service(db, user_id, bank_id)

def delete_bank_account(
    bank_id: int,
    user_id: int = Depends(get_auth_user_id),
    db: Session = Depends(get_db)
):
    return delete_bank_account_service(db, user_id, bank_id)