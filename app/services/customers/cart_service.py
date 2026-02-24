# app/services/customers/cart_service.py
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.trainers.trainer_cart import TrainerCart
from app.models.trainers.trainer_cart_details import TrainerCartDetails
from app.models.trainers.assign_trainer_service import UserService
from app.models.sub_services import SubService
from app.utils.helpers import get_order_date_format


def extract_array(form, key_name):
    """
    Extract Laravel-style array fields:
    service_id[0], service_id[1] → list
    """
    values = []
    for k, v in form.items():
        if k == key_name or k.startswith(f"{key_name}["):
            values.append(v)
    return values

# add trainer Cart Service

def add_to_cart_service(
    db: Session,
    user_id: int,
    form
):
    try:
        # -----------------------------
        # Normal fields
        # -----------------------------
        service_type = int(form.get("service_type"))
        pet_id = int(form.get("pet_id"))
        trainer_id = int(form.get("trainer_id"))
        total_amount = float(form.get("total_amount", 0))

        # -----------------------------
        # Array fields (Laravel style)
        # -----------------------------
        service_ids = extract_array(form, "service_id")
        booking_from = extract_array(form, "booking_from")
        booking_to = extract_array(form, "booking_to")
        booking_time = extract_array(form, "booking_time")

        if not service_ids:
            raise HTTPException(status_code=422, detail="service_id is required")

        # -----------------------------
        # Duplicate service check
        # -----------------------------
        existing_services = (
            db.query(TrainerCartDetails.service_id)
            .join(TrainerCart, TrainerCart.cart_id == TrainerCartDetails.cart_id)
            .filter(TrainerCart.customer_id == user_id)
            .filter(TrainerCart.trainer_id == trainer_id)
            .all()
        )

        existing_services = {s.service_id for s in existing_services}
        common_services = existing_services.intersection(set(map(int, service_ids)))

        if common_services:
            names = (
                db.query(SubService.service_name)
                .filter(SubService.id.in_(common_services))
                .all()
            )

            return {
                "status": False,
                "data": [{"service_name": n.service_name} for n in names],
                "message": "Already Service is added to cart"
            }

        # -----------------------------
        # Create Cart
        # -----------------------------
        cart = TrainerCart(
            service_type=service_type,
            booking_date=booking_from[0],
            booking_to=booking_to[0],
            booking_time=booking_time[0],
            customer_id=user_id,
            pet_id=pet_id,
            trainer_id=trainer_id,
            total_amount=total_amount,
            created_by=user_id,
            created_at=datetime.utcnow()
        )

        db.add(cart)
        db.flush()

        # -----------------------------
        # Cart Details
        # -----------------------------
        cart_details = []

        for i, service_id in enumerate(service_ids):
            price = (
                db.query(UserService.price)
                .filter(UserService.trainer_id == trainer_id)
                .filter(UserService.service_id == service_id)
                .scalar()
            ) or 0

            cart_details.append(
                TrainerCartDetails(
                    cart_id=cart.cart_id,
                    service_id=int(service_id),
                    booking_from=booking_from[i],
                    booking_to=booking_to[i],
                    booking_time=booking_time[i],
                    amount=price,
                    status=1,
                    created_by=user_id,
                    created_at=datetime.utcnow()
                )
            )

        db.add_all(cart_details)
        db.commit()

        return {
            "status": True,
            "message": "Added cart successfully."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Cart Details Service

def cart_details_service(db: Session, user_id: int):
    # -----------------------------
    # Get cart IDs
    # -----------------------------
    cart_ids = (
        db.query(TrainerCart.cart_id)
        .filter(TrainerCart.customer_id == user_id)
        .all()
    )

    cart_ids = [c.cart_id for c in cart_ids]

    if not cart_ids:
        return {
            "status": False,
            "message": "cart is empty"
        }

    # -----------------------------
    # Cart details
    # -----------------------------
    results = (
        db.query(TrainerCartDetails)
        .filter(TrainerCartDetails.cart_id.in_(cart_ids))
        .all()
    )

    cart_details = []
    total_amount = 0

    for row in results:
        amount = float(row.amount or 0)
        total_amount += amount

        service_name = (
        db.query(SubService.service_name)
        .filter(SubService.id == row.service_id)
        .scalar()
    )

        cart_details.append({
            "cart_id": row.cart_id,
            "service_id": row.service_id,
            "service_name": ( service_name if service_name else ""),
            "amount": str(amount),
            "booking_date": get_order_date_format(row.booking_from),
            "booking_time": row.booking_time,
        })

    # -----------------------------
    # Tax calculation
    # -----------------------------
    cgst = 0
    sgst = 0
    service_tax = 0

    cgst_comm = total_amount * cgst / 100
    sgst_comm = total_amount * sgst / 100
    service_tax_comm = total_amount * service_tax / 100

    total_service_taxes = cgst_comm + sgst_comm + service_tax_comm

    bill_details = {
        "sub_total": total_amount,
        "cgst": cgst_comm,
        "sgst": sgst_comm,
        "service_tax": service_tax_comm,
        "service_fee_taxes": total_service_taxes,
        "total_amount": total_amount + total_service_taxes
    }

    return {
        "status": True,
        "data": cart_details,
        "bill_details": bill_details,
        "message": "cart details info."
    }

 
#  Remove Cart service
def remove_service_by_cart(db: Session, user_id: int, service_id: int):
    try:
        # -----------------------------
        # Get cart IDs for user
        # -----------------------------
        cart_ids = (
            db.query(TrainerCart.cart_id)
            .filter(TrainerCart.customer_id == user_id)
            .all()
        )
        cart_ids = [c.cart_id for c in cart_ids]

        if not cart_ids:
            return {
                "status": False,
                "message": "Cart is empty"
            }

        # -----------------------------
        # Delete service from cart
        # -----------------------------
        deleted = (
            db.query(TrainerCartDetails)
            .filter(TrainerCartDetails.service_id == service_id)
            .filter(TrainerCartDetails.cart_id.in_(cart_ids))
            .delete(synchronize_session=False)
        )

        # -----------------------------
        # Service not found
        # -----------------------------
        if deleted == 0:
            db.commit()
            return {
                "status": False,
                "message": "Service not found in cart"
            }

        # -----------------------------
        # Check remaining services
        # -----------------------------
        remaining = (
            db.query(TrainerCartDetails)
            .filter(TrainerCartDetails.cart_id.in_(cart_ids))
            .count()
        )

        # -----------------------------
        # Delete cart if empty
        # -----------------------------
        if remaining == 0:
            (
                db.query(TrainerCart)
                .filter(TrainerCart.customer_id == user_id)
                .delete(synchronize_session=False)
            )

        db.commit()

        return {
            "status": True,
            "message": "removes service from cart."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )


def clear_cart_service(
    db: Session,
    user_id: int,
    trainer_id: int
):
    try:
        # -----------------------------
        # Check if cart exists
        # -----------------------------
        cart_ids = (
            db.query(TrainerCart.cart_id)
            .filter(TrainerCart.customer_id == user_id)
            .filter(TrainerCart.trainer_id == trainer_id)
            .all()
        )

        cart_ids = [c.cart_id for c in cart_ids]

        if not cart_ids:
            return {
                "status": False,
                "message": "Cart is empty"
            }

        # -----------------------------
        # Delete cart details
        # -----------------------------
        db.query(TrainerCartDetails) \
            .filter(TrainerCartDetails.cart_id.in_(cart_ids)) \
            .delete(synchronize_session=False)

        # -----------------------------
        # Delete cart
        # -----------------------------
        db.query(TrainerCart) \
            .filter(TrainerCart.customer_id == user_id) \
            .filter(TrainerCart.trainer_id == trainer_id) \
            .delete(synchronize_session=False)

        db.commit()

        return {
            "status": True,
            "message": "cleared cart."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


