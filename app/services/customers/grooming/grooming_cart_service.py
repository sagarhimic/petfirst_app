from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails
from app.models.Franchises.franchise import Franchise
from app.models.sub_services import SubService


def add_cart(
    db: Session,
    user_id: int,
    service_type: int,
    pet_id: int,
    franchise_id: int,
    service_id: List[int],
    booking_from: List[str],      # form-data always string
    booking_time: List[str],
    total_amount: float
):

    try:
    # 🔹 Existing franchise check
        exist_franchise_id = (
            db.query(GroomingCart.franchise_id)
            .filter(GroomingCart.customer_id == user_id)
            .distinct()
            .scalar()
        )

        if exist_franchise_id and exist_franchise_id != franchise_id:
            fr = db.query(Franchise).filter(
                Franchise.id == exist_franchise_id
            ).first()

            return {
                "status": False,
                "message": (
                    f"{fr.location} - services have been added to an existing cart. "
                    f"If you need another franchise, clear the services in the carts."
                )
            }

        # 🔹 Get cart IDs
        cart_ids = (
            db.query(GroomingCart.cart_id)
            .filter(
                GroomingCart.customer_id == user_id,
                GroomingCart.franchise_id == franchise_id
            )
            .all()
        )
        cart_ids = [c[0] for c in cart_ids]

        # 🔹 Existing services
        if cart_ids:
            existing_services = (
                db.query(GroomingCartDetails.service_id)
                .filter(GroomingCartDetails.cart_id.in_(cart_ids))
                .all()
            )
            existing_services = [s[0] for s in existing_services]
        else:
            existing_services = []

        common_services = set(existing_services) & set(service_id)

        if common_services:
            sub_services = (
                db.query(SubService.service_name)
                .filter(SubService.id.in_(common_services))
                .all()
            )

            return {
                "status": False,
                "data": [{"serice_name": s[0]} for s in sub_services],
                "message": "Already Service is added to cart"
            }

        # 🔹 Convert first booking date safely
        first_booking_date = booking_from[0]
        if isinstance(first_booking_date, str):
            first_booking_date = datetime.strptime(
                first_booking_date, "%Y-%m-%d"
            ).date()

        # 🔹 Create Cart
        cart = GroomingCart(
            franchise_id=franchise_id,
            service_type=service_type,
            booking_date=first_booking_date,
            booking_time=booking_time[0],
            customer_id=user_id,
            pet_id=pet_id,
            total_amount=total_amount,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(cart)
        db.flush()  # same as insertGetId()

        print("CART_ID AFTER FLUSH:", cart.cart_id)

        # 🔹 Cart Details
        details = []

        for i, service in enumerate(service_id):

            price = (
                db.query(SubService.price)
                .filter(SubService.id == service)
                .scalar()
            ) or 0

            booking_date = booking_from[i]
            if isinstance(booking_date, str):
                booking_date = booking_date.strip()
                booking_date = datetime.strptime(
                    booking_date, "%Y-%m-%d"
                ).date()

            booking_dt = datetime.combine(
                booking_date,
                datetime.strptime(booking_time[i].strip(), "%H:%M").time()
            )

            details.append(
                GroomingCartDetails(
                    cart_id=cart.cart_id,
                    service_id=service,
                    booking_from=booking_dt,
                    booking_time=booking_time[i],
                    amount=price,
                    status=1,
                    created_by=user_id,
                    created_at=datetime.utcnow()
                )
            )

        # 🔥 THIS WAS MISSING
        db.add_all(details)
        db.flush()

        db.commit()
        return {
            "status": True,
            "cart_id": cart.cart_id,
            "message": "added cart successfully."
        }
    except Exception as e:
        db.rollback()
        raise e
