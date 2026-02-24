from sqlalchemy.orm import Session

from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails

def clear_cart(
    db: Session,
    user_id: int,
    franchise_id: int
):
    try:
        # 🔹 Get cart IDs for this user & franchise
        cart_ids = (
            db.query(GroomingCart.cart_id)
            .filter(
                GroomingCart.customer_id == user_id,
                GroomingCart.franchise_id == franchise_id
            )
            .all()
        )

        cart_ids = [c[0] for c in cart_ids]

        if not cart_ids:
            return {
                "status": False,
                "message": "cart is empty"
            }

        # 🔹 Delete cart details first
        db.query(GroomingCartDetails).filter(
            GroomingCartDetails.cart_id.in_(cart_ids)
        ).delete(synchronize_session=False)

        # 🔹 Delete carts
        db.query(GroomingCart).filter(
            GroomingCart.cart_id.in_(cart_ids)
        ).delete(synchronize_session=False)

        db.commit()

        return {
            "status": True,
            "message": "cleared cart."
        }

    except Exception as e:
        db.rollback()
        return {
            "status": False,
            "message": "Something went wrong.",
            "errors": str(e)
        }


# Remove service By Cart

def remove_service_by_cart(
    cart_id: int,
    db: Session,
    user_id: int
):
    try:
        # 🔹 Check cart exists
        count = (
            db.query(GroomingCart)
            .filter(GroomingCart.cart_id == cart_id)
            .count()
        )

        if count > 0:
            # 🔹 Delete cart details
            db.query(GroomingCartDetails).filter(
                GroomingCartDetails.cart_id == cart_id
            ).delete(synchronize_session=False)

            # 🔹 Delete cart (only for this user)
            db.query(GroomingCart).filter(
                GroomingCart.cart_id == cart_id,
                GroomingCart.customer_id == user_id
            ).delete(synchronize_session=False)

        db.commit()

        return {
            "status": True,
            "message": "removes service from cart."
        }

    except Exception as e:
        db.rollback()
        return {
            "status": False,
            "message": "Something went wrong.",
            "errors": f"{str(e)}"
        }
