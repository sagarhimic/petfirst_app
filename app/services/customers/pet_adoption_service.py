from app.schemas.customers.pet_adoption_schema import PetFilterRequest, StorePetAdoptionRequest
from sqlalchemy.orm import Session

from fastapi import Request, HTTPException, UploadFile, Depends, File, Form, APIRouter
from app.models.user import User
from app.models.Petadoption.enquiry import Enquiry
from app.models.online_pets import OnlinePets
from app.models.Petadoption.enquiry_details import EnquiryDetail
from app.models.Notifications.notifications import Notification
from app.models.Notifications.notification_users import NotificationUser
from datetime import datetime
from sqlalchemy import or_, func, cast, String
from app.utils.helpers import format_date_db, get_order_date_format

from math import radians, cos, sin, acos
from app.models.user_location import UserLocation
from app.models.user_personal_info import UserPersonalInfo
from sqlalchemy.sql import text
from app.models.online_pet_images import OnlinePetImages
from app.models.online_pets_behavior import OnlinePetsBehavior
from app.models.pet_types import PetTypes
#from app.utils.pet_categories import get_pet_categories
#from app.core.config import SECRET_KEY
from math import radians

SECRET_KEY = "PETFIRST_SECRET"
from app.core.database import get_db
from app.core.config import settings
from sqlalchemy.orm import joinedload

from jose import jwt
from math import radians
from typing import Dict, Any

EARTH_RADIUS = 6371 

def add_enquiry_service(
    db: Session,
    user_id: int,
    pet_adoption_id: int,
    data: StorePetAdoptionRequest
):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        # Fetch pet info
        pet = (
            db.query(OnlinePets)
            .filter(OnlinePets.product_id == pet_adoption_id)
            .first()
        )

        if not pet:
            raise HTTPException(
                status_code=404,
                detail={"status": False, "message": "Pet not found"}
            )

        # Create enquiry
        enquiry = Enquiry(
            service_type=1,
            customer_id=user_id,
            full_name=data.full_name,
            email=data.email,
            mobile=data.mobile,
            seller_id=pet.owner_id,
            franchise_id=None,
            enquiry_date=datetime.utcnow(),
            status_id=1,
            contact_method=data.contact_method,
            time_to_contact=data.time_to_contact,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(enquiry)
        db.flush()  # To get enquiry_id
        enquiry_id = enquiry.enquiry_id

        # Enquiry detail
        enquiry_detail = EnquiryDetail(
            enquiry_id=enquiry_id,
            product_id=pet.product_id
        )
        db.add(enquiry_detail)

        # Notification
        notification = Notification(
            type_id=1,
            title=f"Pet Adoption: Customer Enquired Pet Adoption - {enquiry_id}",
            link=f"seller/get-order-details/{enquiry_id}",
            enquiry_id=enquiry_id,
            status_id=1,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.flush()

        # Notification user
        notification_user = NotificationUser(
            noti_id=notification.id,
            seller_id=pet.owner_id,
            status=1,
            management_status=1
        )
        db.add(notification_user)

        db.commit()

        return {
            "status": True,
            "enquiry_id": enquiry_id,
            "message": "We will contact you shortly, Thank you."
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

def enquiries_list_service(
    db: Session,
    user_id: int,
    search_key: str = "",
    status_id: str = "",
    date_from: str = "",
    date_to: str = "",
    request: Request = None
):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
        # -----------------------------
        # Date conversion
        # -----------------------------
        if date_from:
            date_from = format_date_db(date_from)

        if date_to:
            date_to = format_date_db(date_to)

        # -----------------------------
        # Base Query
        # -----------------------------
        query = db.query(Enquiry).filter(
            Enquiry.customer_id == user_id
        )

        # -----------------------------
        # Search Filter
        # -----------------------------
        if search_key:
            query = query.filter(
                or_(
                    cast(Enquiry.enquiry_id, String).ilike(f"%{search_key}%"),
                    Enquiry.seller.has(
                        func.lower(User.name).ilike(f"%{search_key.lower()}%")
                    )
                )
            )

        # -----------------------------
        # Date Filter
        # -----------------------------
        if date_from and not date_to:
            query = query.filter(
                func.date(Enquiry.enquiry_date) >= date_from
            )

        if date_from and date_to:
            query = query.filter(
                func.date(Enquiry.enquiry_date).between(date_from, date_to)
            )

        # -----------------------------
        # Status Filter
        # -----------------------------
        if status_id:
            query = query.filter(
                Enquiry.status_id == status_id
            )

        # -----------------------------
        # Pagination
        # -----------------------------
        page = 1
        per_page = 10

        results = (
            query.order_by(Enquiry.enquiry_date.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        total_items = query.count()

        # -----------------------------
        # Response Formatting
        # -----------------------------
        enquiries_list = []

        for record in results:
            enquiries_list.append({
                "seller": record.seller.name if record.seller else "",
                "enquiry_id": record.enquiry_id,
                "pet_name": (
                    record.enquiry_details.product.breed_name.name
                    if record.enquiry_details
                    and record.enquiry_details.product
                    and record.enquiry_details.product.breed_name
                    else ""
                ),
                "service_type": (
                    record.servicetype.service_name
                    if record.servicetype else ""
                ),
                "enquiry_date": get_order_date_format(record.enquiry_date),
                "customer_name": (
                    record.customer.name
                    if record.customer else ""
                ),
                "status": (
                    record.status.name
                    if record.status else ""
                ),
                "status_color": (
                    record.status.color
                    if record.status else ""
                )
            })

        return {
            "status": True,
            "data": enquiries_list,
            "message": "Enquiries Info.",
            "total": total_items,
            "per_page": per_page,
            "current_page": page,
            "last_page": (total_items + per_page - 1) // per_page,
            "has_more_pages": total_items > per_page
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "status": False,
                "message": "Something went wrong",
                "error": str(e)
            }
        )
    
def get_online_pets_list_service(
    db: Session,
    user_id: int,
    data: PetFilterRequest
):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    pet_filters = {
        "pet_types": data.pet_types or [],
        "pet_size": data.size or [],
        "pet_gender": data.gender or [],
        "pet_breed": data.breeds or [],
        "pet_color": data.colors or [],
        "pet_age_from": None,
        "pet_age_to": None,
    }

    if data.age and "-" in data.age:
        pet_filters["pet_age_from"], pet_filters["pet_age_to"] = map(
            int, data.age.split("-")
        )

    latitude = radians(float(data.latitude or 0))
    longitude = radians(float(data.longitude or 0))
    radius = 10

    nearby = get_nearby_online_pet_locations(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        pet_filters=pet_filters,
        user_id=user_id
    )

    results = []

    for row in nearby["items"]:
        pet = row[0]
        user_name = row[1]
        mobile = row[2]
        location = row[3]
        profile_pic = row[4]
        distance = row[5]

        images = db.query(OnlinePetImages).filter(
            OnlinePetImages.product_id == pet.product_id
        ).all()

        behaviors = db.query(OnlinePetsBehavior).filter(
            OnlinePetsBehavior.online_pet_id == pet.product_id
        ).all()

        behavior_names = list({
            b.behavior.name for b in behaviors if b.behavior
        })

        results.append({
            "product_id": pet.product_id,
            "pet_name": pet.breed_name.name if pet.breed_name else None,
            "age": pet.age,
            "breed": pet.breed_name.name if pet.breed_name else None,
            "color": pet.color_name.name if pet.color_name else None,
            "height": pet.height,
            "weight": pet.weight,
            "price": pet.price,
            "status": "Available" if pet.status == 1 else "Not Available",
            "gender": pet.genderinfo.name if pet.genderinfo else None,
            "pet_type": pet.pettype.name if pet.pettype else None,
            "size": pet.size,
            "vaccine": "YES" if pet.vaccine == 1 else "NO",
            "pet_story": pet.pet_story,
            "personality": pet.personality,
            "health": pet.health,
            "compatibility": pet.compatibility,
            "life_span_from": pet.life_span_from,
            "life_span_to": pet.life_span_to,
            "behaviors": behavior_names or None,
            "image_data": images or None,
            "name": user_name,
            "mobile": mobile,
            "profile_pic": profile_pic,
            "location": location,
            "distance": f"{round(distance, 2)} kms"
        })

    return {
        "status": True,
        "data": results,
        "category": get_pet_categories(db),
        "message": "Pets Info" if results else "No records found",
        **nearby
    }

def get_nearby_online_pet_locations(
    db: Session,
    latitude: float,
    longitude: float,
    radius: int,
    pet_filters: dict,
    user_id: int
):
    distance = (
        EARTH_RADIUS * func.acos(
            func.cos(latitude)
            * func.cos(func.radians(UserLocation.latitude))
            * func.cos(func.radians(UserLocation.longitude) - longitude)
            + func.sin(latitude)
            * func.sin(func.radians(UserLocation.latitude))
        )
    ).label("distance")

    query = (
        db.query(
            OnlinePets,
            User.name.label("user_name"),
            User.mobile,
            UserLocation.location,
            UserPersonalInfo.profile_pic,
            distance
        )
        .join(User, User.id == OnlinePets.owner_id)
        .outerjoin(
            UserLocation,
            (UserLocation.user_id == OnlinePets.owner_id)
            & (UserLocation.latitude.isnot(None))
            & (UserLocation.longitude.isnot(None))
        )
        .outerjoin(UserPersonalInfo, UserPersonalInfo.user_id == OnlinePets.owner_id)
        .filter(
            OnlinePets.status == 1,
            User.status == 1,
            OnlinePets.owner_id != user_id,
            distance <= radius
        )
        .order_by(distance)
    )

    if pet_filters["pet_types"]:
        query = query.filter(OnlinePets.pet_type.in_(pet_filters["pet_types"]))

    if pet_filters["pet_size"]:
        query = query.filter(OnlinePets.size.in_(pet_filters["pet_size"]))

    if pet_filters["pet_gender"]:
        query = query.filter(OnlinePets.gender.in_(pet_filters["pet_gender"]))

    if pet_filters["pet_age_from"] is not None:
        query = query.filter(
            OnlinePets.age.between(
                pet_filters["pet_age_from"],
                pet_filters["pet_age_to"]
            )
        )

    records = query.all()
    return paginate_results(records, 10)


def paginate_results(records, per_page):
    total = len(records)
    return {
        "total": total,
        "per_page": per_page,
        "pages": (total // per_page) + (1 if total % per_page else 0),
        "items": records[:per_page],
        "has_more_pages": total > per_page
    }


def get_pet_categories(db: Session):
    pet_counts = (
        db.query(
            PetTypes.id,
            PetTypes.name,
            func.count(OnlinePets.pet_type).label("total")
        )
        .outerjoin(
            OnlinePets,
            (OnlinePets.pet_type == PetTypes.id) &
            (OnlinePets.status == 1)
        )
        .filter(PetTypes.id.in_([1, 2]))
        .group_by(PetTypes.id, PetTypes.name)
        .all()
    )

    result = [{
        "pet_type": p.id,
        "pet_name": p.name,
        "count": p.total
    } for p in pet_counts]

    for pid, name in [(1, "Dog"), (2, "Cat")]:
        if not any(p["pet_type"] == pid for p in result):
            result.append({
                "pet_type": pid,
                "pet_name": name,
                "count": 0
            })

    return result

def pet_adoption_details_service(
    pet_id: int,
    user_id: int,
    db: Session
):
    if not user_id:
        return {"status": False, "message": "Access Denied"}

    try:
         # Fetch pet
      
        onlinepet = (
            db.query(OnlinePets)
            .options(
                joinedload(OnlinePets.owner)
                .joinedload(User.locations)
            )
            .filter(OnlinePets.product_id == pet_id)
            .first()
        )

        if not onlinepet:
            raise HTTPException(
                status_code=404,
                detail={"status": False, "message": "Pet not found"}
            )

        # Pricing calculation
        entry_fee = onlinepet.price or 0
        cgst = 0
        sgst = 0
        service_tax = settings.CUSTOMER_SIDE_COMMISSION  # constants
      

        calculation_results = total_price(
            entry_fee=entry_fee,
            cgst=cgst,
            sgst=sgst,
            service_tax=service_tax
        )

        fee_details = {
            "pet_price": int(onlinepet.price or 0),
            "cgst": calculation_results["cgst_fee"],
            "sgst": calculation_results["sgst_fee"],
            "service_tax": calculation_results["service_tax"],
            "service_tax_and_fee": (
                calculation_results["service_tax"]
                + calculation_results["cgst_fee"]
                + calculation_results["sgst_fee"]
            ),
            "total_amount": calculation_results["total_amount"],
        }

        # Images
        onlinepets_images = (
            db.query(OnlinePetImages)
            .filter(OnlinePetImages.product_id == onlinepet.product_id)
            .all()
        )

        # Behaviors
        behaviors = (
            db.query(OnlinePetsBehavior)
            .filter(OnlinePetsBehavior.online_pet_id == onlinepet.product_id)
            .all()
        )

        behavior_names = list({
            b.behavior.name
            for b in behaviors
            if b.behavior and b.behavior.name
        })

        # Primary seller location
        primary_location = None
        if onlinepet.owner and onlinepet.owner.locations:
            primary_location = next(
                (loc for loc in onlinepet.owner.locations if loc.is_primary == 1),
                None
            )

        response_data = {
            "id": onlinepet.product_id,
            "seller_name": onlinepet.owner.name if onlinepet.owner else None,
            "seller_city": primary_location.city if primary_location else None,
            "pet_name": onlinepet.breed_name.name if onlinepet.breed_name else None,
            "age": onlinepet.age,
            "dob": onlinepet.dob,
            "breed": onlinepet.breed_name.name if onlinepet.breed_name else None,
            "color": onlinepet.color_name.name if onlinepet.color_name else None,
            "height": onlinepet.height,
            "weight": onlinepet.weight,
            "price": onlinepet.price,
            "quantity": onlinepet.quantity,
            "description": onlinepet.description,
            "gender": onlinepet.genderinfo.name if onlinepet.genderinfo else None,
            "pet_type": onlinepet.pettype.name if onlinepet.pettype else None,
            "size": pet_size(onlinepet.size) if onlinepet.size else None,
            "vaccine": "Yes" if onlinepet.vaccine == 1 else "No" if onlinepet.vaccine == 2 else "",
            "pet_story": onlinepet.pet_story,
            "personality": onlinepet.personality,
            "health": onlinepet.health,
            "compatibility": onlinepet.compatibility,
            "life_span_from": onlinepet.life_span_from,
            "life_span_to": onlinepet.life_span_to,
            "delivery_type": "Home" if onlinepet.delivery_type == 1 else "Pet Store" if onlinepet.delivery_type == 2 else "",
            "behaviors": behavior_names if behavior_names else None,
            "image_data": onlinepets_images if onlinepets_images else None,
            "status": 1,
            "created_by": user_id,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

        return {
            "status": True,
            "data": response_data,
            "payment_details": fee_details
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
                "error": str(e)
            }
        )
    
def total_price(entry_fee, cgst, sgst, service_tax):
    service_tax_fee = (entry_fee * service_tax) / 100
    total_amount = entry_fee + cgst + sgst + service_tax_fee

    return {
        "cgst_fee": cgst,
        "sgst_fee": sgst,
        "service_tax": service_tax_fee,
        "total_amount": total_amount
    }

def pet_size(size):
    return {
        1: "Small",
        2: "Medium",
        3: "Large"
    }.get(size, None)

    

