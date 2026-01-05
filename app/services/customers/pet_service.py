from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import UploadFile, HTTPException
import os
import shutil

from app.models.pet_info import PetInfo

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB (adjust to your config)

def store_pet_service(
    db: Session,
    data,
    file: UploadFile | None,
    user_id: int
):
    try:
        # 🔐 BEGIN TRANSACTION
        if data.is_primary == 1:
            db.query(PetInfo).filter(
                PetInfo.owner_id == user_id,
                PetInfo.is_primary == 1
            ).update({"is_primary": None})

        pet = PetInfo(
            owner_id=user_id,
            pet_type=data.pet_type,
            pet_name=data.pet_name,
            age_yr=data.age_yr,
            age_month=data.age_month,
            dob=data.dob,
            breed=data.breed,
            color=data.color,
            height=data.height,
            weight=data.weight,
            gender=data.gender,
            is_primary=data.is_primary,
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
