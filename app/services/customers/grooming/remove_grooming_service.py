from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails


def remove_service(
    db: Session,
    user_id: int,
    service_id: int
):
    try:
        # --------------------------------
        # Get all cart ids for user
        # --------------------------------
        cart_ids = (
            db.query(GroomingCart.cart_id)
            .filter(GroomingCart.customer_id == user_id)
            .all()
        )

        cart_ids = [c.cart_id for c in cart_ids]

        if not cart_ids:
            return {
                "status": False,
                "message": "Cart not found"
            }

        # --------------------------------
        # Check service exists in cart
        # --------------------------------
        gr_service = (
            db.query(GroomingCartDetails)
            .filter(GroomingCartDetails.cart_id.in_(cart_ids))
            .filter(GroomingCartDetails.service_id == service_id)
            .first()
        )

        if not gr_service:
            return {
                "status": False,
                "message": "Service not found in cart"
            }

        # --------------------------------
        # Delete cart details
        # --------------------------------
        db.query(GroomingCartDetails) \
            .filter(GroomingCartDetails.service_id == gr_service.service_id) \
            .delete(synchronize_session=False)

        # --------------------------------
        # Delete cart
        # --------------------------------
        db.query(GroomingCart) \
            .filter(GroomingCart.cart_id == gr_service.cart_id) \
            .delete(synchronize_session=False)

        db.commit()

        return {
            "status": True,
            "message": "service removed"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
