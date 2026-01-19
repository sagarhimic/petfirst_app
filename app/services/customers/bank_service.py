from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, UploadFile
from app.models.user import User
from app.models.bank_info import CustomerBankDetails

from datetime import datetime
import os, shutil

def get_bank_details_service(db: Session, user_id: int, request: Request):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        banks = (
            db.query(CustomerBankDetails)
            .filter(CustomerBankDetails.user_id == user_id)
            .order_by(CustomerBankDetails.is_primary.desc())
            .all()
        )
        print(banks)

        results = []
        for bank in banks:
            results.append({
                "bank_id": bank.id,
                "user_id": bank.user_id,
                "account_holder_name": bank.account_holder_name or None,
                "account_number": bank.account_number or None,
                "bank_name": bank.bank_name or None,
                "ifsc": bank.ifsc or None,
                "recipient_id": bank.recipient_id or None,
                "is_primary": "Active" if bank.is_primary == 1 else None
            })
    

        return {
            "status": True,
            "data": results,
            "message": "Bank Details Info."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "message": "Something went wrong",
                "errors": str(e)
            }
        )
    
def add_bank_details_service(db: Session, user_id: int, data):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        # Save new record
        new_bank = CustomerBankDetails(
            user_id=user_id,
            bank_name=data.bank_name,
            account_holder_name=data.account_holder_name,
            account_number=data.account_number,
            ifsc=data.ifsc,
            is_primary=1,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(new_bank)
        db.commit()
        db.refresh(new_bank)

        # Make all other banks non-primary
        db.query(CustomerBankDetails).filter(
            CustomerBankDetails.user_id == user_id,
            CustomerBankDetails.id != new_bank.id
        ).update({"is_primary": None})

        db.commit()

        return {
            "status": True,
            "data": {
                "bank_id": new_bank.id,
                "user_id": new_bank.user_id,
                "account_holder_name": new_bank.account_holder_name,
                "account_number": new_bank.account_number,
                "bank_name": new_bank.bank_name,
                "ifsc": new_bank.ifsc,
                "recipient_id": new_bank.recipient_id,
                "is_primary": "Active" if new_bank.is_primary == 1 else None
            },
            "message": "Bank Details Added Successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "message": "Something went wrong",
                "errors": str(e)
            }
        )
    
def update_bank_primary_service(db: Session, user_id: int, bank_id: int):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
       # First update this bank to primary
        updated = (
            db.query(CustomerBankDetails)
            .filter(CustomerBankDetails.user_id == user_id,
                    CustomerBankDetails.id == bank_id)
            .update({CustomerBankDetails.is_primary: 1})
        )

        if updated == 0:
            raise HTTPException(status_code=404, detail={"status": False, "message": "Bank not found"})

        # Remove primary from all other bank accounts of user
        db.query(CustomerBankDetails).filter(
            CustomerBankDetails.user_id == user_id,
            CustomerBankDetails.id != bank_id
        ).update({CustomerBankDetails.is_primary: None})

        db.commit()

        return {
            "status": True,
            "message": "Updated as Primary."
        }


    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "message": "Something went wrong",
                "errors": str(e)
            }
        )
    
def delete_bank_account_service(db: Session, user_id: int, bank_id: int):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        # Check if this bank is primary
        is_primary = db.query(CustomerBankDetails).filter(
            CustomerBankDetails.id == bank_id,
            CustomerBankDetails.user_id == user_id,
            CustomerBankDetails.is_primary == 1
        ).count()

        if is_primary > 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": False,
                    "message": "Please update to another primary account before deleting this account."
                }
            )

        # Delete bank
        db.query(CustomerBankDetails).filter(
            CustomerBankDetails.user_id == user_id,
            CustomerBankDetails.id == bank_id
        ).delete()

        db.commit()

        return {
            "status": True,
            "message": "Bank account deleted successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "message": "Something went wrong",
                "errors": str(e)
            }
        )