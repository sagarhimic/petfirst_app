from sqlalchemy.orm import Session
from datetime import datetime

from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails
from app.utils.helpers import format_date_db


def modify_service_by_cart(
    db: Session,
    user_id: int,
    cart_id: int,
    booking_from: str = None,
    booking_time: str = None
):
    try:
        modify_cart_data = {
            "booking_date": format_date_db(booking_from) if booking_from else None,
            "booking_time": booking_time,
            "updated_by": user_id,
            "updated_at": datetime.utcnow()
        }

        # 🔹 Update cart
        update_cart_count = (
            db.query(GroomingCart)
            .filter(GroomingCart.cart_id == cart_id)
            .update(modify_cart_data, synchronize_session=False)
        )

        if update_cart_count > 0:
            cart_details_update = {
                "booking_from": format_date_db(booking_from),
                "booking_time": booking_time,
                "updated_at": datetime.utcnow(),
                "updated_by": user_id
            }

            # 🔹 Update cart details
            db.query(GroomingCartDetails).filter(
                GroomingCartDetails.cart_id == cart_id
            ).update(cart_details_update, synchronize_session=False)

        db.commit()

        return {
            "status": True,
            "message": "Modified Service Successfully."
        }

    except Exception as e:
        db.rollback()
        return {
            "status": False,
            "message": "Something went wrong.",
            "errors": f"{str(e)}"
        }