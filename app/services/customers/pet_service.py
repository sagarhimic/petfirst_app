from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import UploadFile, HTTPException, Request
import os
import shutil
from sqlalchemy import desc
from typing import Optional
from app.utils.helpers import format_date

from app.models.pet_info import PetInfo
from app.models.pet_types import PetTypes
from app.models.breeds import Breeds
from app.models.colors import Colors
from app.models.gender_info import GenderInfo

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB (adjust to your config)

def store_pet_service(
    db: Session,
    data: dict,
    file: UploadFile | None,
    user_id: int
):
    try:
        # 🔐 BEGIN TRANSACTION
         # ✅ FIX HERE
        if data.get("is_primary") == 1:
            db.query(PetInfo).filter(
                PetInfo.owner_id == user_id,
                PetInfo.is_primary == 1
            ).update({"is_primary": None})

        pet = PetInfo(
            owner_id=user_id,
            pet_type=data.get("pet_type"),
            pet_name=data.get("pet_name"),
            age_yr=data.get("age_yr"),
            age_month=data.get("age_month"),
            dob=data.get("dob"),
            breed=data.get("breed"),
            color=data.get("color"),
            height=data.get("height"),
            weight=data.get("weight"),
            gender=data.get("gender"),
            is_primary=data.get("is_primary"),
            created_at=datetime.utcnow(),
            created_by=user_id
        )

        db.add(pet)
        db.flush()  # ✅ get pet.id before commit

        # 📸 FILE UPLOAD (Same as Laravel)
        if file:
            ext = file.filename.split(".")[-1].lower()

            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail="Only jpg, jpeg, png files are allowed"
                )

            contents = file.file.read()
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="Picture size exceeds allowed limit"
                )

            # Folder structure
            base_path = f"uploads/customers/pets/{user_id}/{datetime.now().strftime('%Y/%m')}"
            os.makedirs(base_path, exist_ok=True)

            filename = f"Pet_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            file_path = os.path.join(base_path, filename)

            with open(file_path, "wb") as f:
                f.write(contents)

            pet.pet_profile_pic = file_path

        db.commit()

        return {
            "status": True,
            "pet_id": pet.id,
            "message": "Pet Info added successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def update_pet_pic_service(
    db: Session,
    pet_id: int,
    file: UploadFile,
    user_id: int
):
    try:
        # 🔍 Check pet belongs to user
        pet = (
            db.query(PetInfo)
            .filter(PetInfo.id == pet_id, PetInfo.owner_id == user_id)
            .first()
        )

        if not pet:
            raise HTTPException(status_code=403, detail="Access Denied")

        # 📄 Validate extension
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only pdf, jpg, jpeg, png files are allowed"
            )

        # 📏 Validate size
        contents = file.file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Picture size exceeds allowed limit"
            )

        # 🗂 Folder structure
        folder_path = f"uploads/customers/pets/{user_id}/{datetime.now().strftime('%Y/%m')}"
        os.makedirs(folder_path, exist_ok=True)

        filename = f"pet_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        new_path = os.path.join(folder_path, filename)

        # 🗑 Delete old image
        if pet.pet_profile_pic and os.path.exists(pet.pet_profile_pic):
            os.remove(pet.pet_profile_pic)

        # 💾 Save new image
        with open(new_path, "wb") as f:
            f.write(contents)

        # 📝 Update DB
        pet.pet_profile_pic = new_path
        pet.updated_at = datetime.utcnow()
        pet.updated_by = user_id

        db.commit()

        return {
            "status": True,
            "message": "Pet Pic Updated Successfully."
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong."
        )

def pet_details_service(
    db: Session,
    user_id: int,
    request: Request,
    search_key: Optional[str] = None,
    pet_type: Optional[int] = None
):
    try:
        query = (
            db.query(
                PetInfo.id.label("pet_id"),
                PetInfo.pet_name,
                PetInfo.age_yr,
                PetInfo.age_month,
                PetInfo.dob,
                PetInfo.height,
                PetInfo.weight,
                PetInfo.is_primary,
                PetInfo.pet_profile_pic,

                PetTypes.name.label("pet_type"),
                Breeds.name.label("breed"),
                Colors.name.label("color"),
                GenderInfo.name.label("gender"),
            )
            .outerjoin(PetTypes, PetInfo.pet_type == PetTypes.id)
            .outerjoin(Breeds, PetInfo.breed == Breeds.id)
            .outerjoin(Colors, PetInfo.color == Colors.id)
            .outerjoin(GenderInfo, PetInfo.gender == GenderInfo.id)
            .filter(PetInfo.owner_id == user_id)
        )

        if search_key:
            query = query.filter(PetInfo.pet_name.ilike(f"%{search_key}%"))

        if pet_type is not None:
            query = query.filter(PetInfo.pet_type == pet_type)

        results = query.order_by(desc(PetInfo.is_primary)).all()

        if not results:
            return {
                "status": False,
                "message": "No Data Found!",
                "data": []
            }

        base_url = str(request.base_url)
        pet_details = []

        for r in results:
            pet_details.append({
                "pet_id": r.pet_id,
                "pet_type": r.pet_type,
                "pet_name": r.pet_name,
                "age": (
                    f"{r.age_yr}Y {r.age_month}M"
                    if r.age_yr or r.age_month else None
                ),
                "dob": format_date(r.dob),
                "breed": r.breed,
                "color": r.color,
                "height": float(r.height) if r.height else None,
                "weight": r.weight,
                "gender": r.gender,
                "pet_profile_pic": (
                    base_url + r.pet_profile_pic.lstrip("/")
                    if r.pet_profile_pic else None
                ),
                "is_primary": r.is_primary
            })

        return {
            "status": True,
            "message": "Pet details list.",
            "data": pet_details
        }

    except Exception as e:
        print("PET DETAILS ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

def edit_pet_service(
    db: Session,
    user_id: int,
    pet_id: int,
    request: Request
):
    try:
        result = (
            db.query(
                PetInfo.id.label("pet_id"),
                PetInfo.pet_name,
                PetInfo.age_yr,
                PetInfo.age_month,
                PetInfo.dob,
                PetInfo.height,
                PetInfo.weight,
                PetInfo.is_primary,
                PetInfo.pet_profile_pic,
                PetTypes.name.label("pet_type"),
                Breeds.name.label("breed"),
                Colors.name.label("color"),
                GenderInfo.name.label("gender"),
            )
            .outerjoin(PetTypes, PetInfo.pet_type == PetTypes.id)
            .outerjoin(Breeds, PetInfo.breed == Breeds.id)
            .outerjoin(Colors, PetInfo.color == Colors.id)
            .outerjoin(GenderInfo, PetInfo.gender == GenderInfo.id)
            .filter(PetInfo.id == pet_id, PetInfo.owner_id == user_id)
            .first()
        )

        if not result:
            return {
                "status": False,
                "message": "No Data Found!",
                "data": []
            }

        base_url = str(request.base_url)
        
        pet_details = {
            "pet_id": result.pet_id,
            "pet_type": result.pet_type,
            "pet_name": result.pet_name,
            "age": (
                f"{result.age_yr}Y {result.age_month}M"
                if result.age_yr or result.age_month else None
            ),
            "dob": format_date(result.dob),
            "breed": result.breed,
            "color": result.color,
            "height": float(result.height) if result.height else None,
            "weight": result.weight,
            "gender": result.gender,
            "pet_profile_pic": (
                base_url + result.pet_profile_pic.lstrip("/")
                if result.pet_profile_pic else None
            ),
            "is_primary": result.is_primary
        }

        return {
            "status": True,
            "message": "Edit Pet Info.",
            "data": pet_details
        }

    except Exception as e:
        print("PET DETAILS ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

def update_pet_service(
    db: Session,
    pet_id: int,
    user_id: int,
    data,
    file: UploadFile | None
):
    try:
        pet = (
            db.query(PetInfo)
            .filter(PetInfo.id == pet_id, PetInfo.owner_id == user_id)
            .first()
        )

        if not pet:
            raise HTTPException(status_code=403, detail="Access Denied")

        # 🔹 Update fields
        pet.pet_type = data.pet_type
        pet.pet_name = data.pet_name
        pet.age_yr = data.age_yr
        pet.age_month = data.age_month
        pet.dob = data.dob
        pet.breed = data.breed
        pet.color = data.color
        pet.height = data.height
        pet.weight = data.weight
        pet.gender = data.gender
        pet.is_primary = data.is_primary
        pet.updated_by = user_id
        pet.updated_at = datetime.utcnow()

        db.flush()

        # 🔹 If primary → unset others
        if data.is_primary == 1:
            db.query(PetInfo).filter(
                PetInfo.owner_id == user_id,
                PetInfo.id != pet_id
            ).update({"is_primary": None})

        # 🔹 Handle file upload
        if file:
            ext = file.filename.split(".")[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail="Only jpg, jpeg, png files are allowed"
                )

            contents = file.file.read()
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="Picture size exceeded limit"
                )

            folder = f"uploads/customers/pets/{user_id}/{datetime.now().strftime('%Y/%m')}"
            os.makedirs(folder, exist_ok=True)

            # delete old
            if pet.pet_profile_pic and os.path.exists(pet.pet_profile_pic):
                os.remove(pet.pet_profile_pic)

            filename = f"Pet_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            path = os.path.join(folder, filename)

            with open(path, "wb") as f:
                f.write(contents)

            pet.pet_profile_pic = path

        db.commit()

        return {
            "status": True,
            "pet_id": pet_id,
            "message": "Pet Info updated successfully."
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def pet_update_primary_service(
    db: Session,
    user_id: int,
    data
):
    try:
        # 🔹 Set selected pet as primary
        updated = (
            db.query(PetInfo)
            .filter(
                PetInfo.owner_id == user_id,
                PetInfo.id == data.pet_id
            )
            .update({"is_primary": 1})
        )

        if updated == 0:
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        # 🔹 Reset other pets
        db.query(PetInfo).filter(
            PetInfo.owner_id == user_id,
            PetInfo.id != data.pet_id
        ).update({"is_primary": None})

        db.commit()

        return {
            "status": True
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong."
        )

