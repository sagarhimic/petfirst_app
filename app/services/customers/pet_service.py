from sqlalchemy.orm import Session
from app.models.pet_info import PetInfo

def save_pet_details(db: Session, data, user_id: int):

    # insert
    pet_details = PetInfo(
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
        pet_profile_pic=data.pet_profile_pic,
        status=data.status,
        is_primary=data.is_primary,
        created_at=datetime.utcnow(),
        created_by = user_id
    )
    db.add(pet_details)

    db.commit()
    return True
