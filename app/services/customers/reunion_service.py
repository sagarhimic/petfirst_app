from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, UploadFile
from app.models.user import User
from app.models.pet_parents import PetParents
from app.utils.helpers import parent_types

from datetime import datetime
import os, shutil

def get_pet_parent_service(db: Session, user_id: int, request: Request):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        pet_parents = db.query(PetParents).filter(PetParents.user_id == user_id).all()

        pet_parent_list = []
        for parent in pet_parents:
            pet_parent_list.append({
                "id": parent.id,
                "pet_id": parent.pet_id,
                "pet_name": parent.pet_name,
                "full_name": parent.full_name,
                "mobile": parent.mobile,
                "email": parent.email,
                "address": parent.address,
                "state_id": parent.state_id,
                "city": parent.city,
                "country_id": parent.country_id,
                "pincode": parent.pincode, 
            })

        return {
            "status": True,
            "data": pet_parent_list,
            "message": "Pet Parents Info."
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

def add_pet_parent_service(db: Session, user_id: int, payload):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        pet_parent_data = PetParents(
            pet_id=payload.pet_id,
            pet_name=payload.pet_parent_name,
            full_name=payload.parent_owner_name,
            mobile=payload.parent_mobile,
            email=payload.parent_email,
            address=payload.address,
            state_id=payload.state_id,
            city=payload.city,
            country_id=payload.country_id,
            pincode=payload.pincode,
            parent_type=payload.parent_type,
            status=1,
            user_id=user_id,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(pet_parent_data)
        db.commit()
        db.refresh(pet_parent_data)

        return {
            "status": True,
            "message": "Pet Parent added successfully."
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
    
def edit_pet_parent_service(db: Session, user_id: int, pet_parent_id: int, request: Request):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        pet_parent = db.query(PetParents).filter(PetParents.id == pet_parent_id, PetParents.user_id == user_id).first()

        if not pet_parent:
            return {
                "status": False,
                "message": "Pet Parent not found."
            }

        pet_parent_data = {
            "id": pet_parent.id,
            "pet_id": pet_parent.pet_id,
            "pet_name": pet_parent.pet_name,
            "full_name": pet_parent.full_name,
            "mobile": pet_parent.mobile,
            "email": pet_parent.email,
            "address": pet_parent.address,
            "state_id": pet_parent.state_id,
            "city": pet_parent.city,
            "country_id": pet_parent.country_id,
            "pincode": pet_parent.pincode,
            "parent_type": pet_parent.parent_type,
            "status": pet_parent.status
        }

        return {
            "status": True,
            "data": pet_parent_data,
            "message": "Pet Parent Info."
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
    
def update_pet_parent_service(db: Session, user_id: int, pet_parent_id: int, payload):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        pet_parent = db.query(PetParents).filter(PetParents.id == pet_parent_id, PetParents.user_id == user_id).first()

        if not pet_parent:
            return {
                "status": False,
                "message": "Pet Parent not found."
            }

        pet_parent.pet_id = payload.pet_id
        pet_parent.pet_name = payload.pet_parent_name
        pet_parent.full_name = payload.pet_parent_owner_name
        pet_parent.mobile = payload.parent_mobile
        pet_parent.email = payload.parent_email
        pet_parent.address = payload.address
        pet_parent.state_id = payload.state_id
        pet_parent.city = payload.city
        pet_parent.country_id = payload.country_id
        pet_parent.pincode = payload.pincode
        pet_parent.parent_type = payload.parent_type
        pet_parent.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(pet_parent)

        return {
            "status": True,
            "message": "Pet Parent updated successfully."
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
    
def delete_pet_parent_service(db: Session, user_id: int, pet_parent_id: int):

    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        pet_parent = (
            db.query(PetParents)
            .filter(PetParents.id == pet_parent_id, PetParents.user_id == user_id)
            .first()
        )

        if not pet_parent:
            return {
                "status": False,
                "message": "Pet Parent not found."
            }

        db.delete(pet_parent)
        db.commit()

        return {
            "status": True,
            "message": "Pet Parent deleted successfully."
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