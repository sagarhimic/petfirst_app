from sqlalchemy.orm import Session
from datetime import datetime

from app.models.Franchises.Grooming.grooming_cart import GroomingCart
from app.models.Franchises.Grooming.grooming_cart_details import GroomingCartDetails
from app.models.user_location import UserLocation
from app.utils.common import get_nearby_franchise_info
from app.utils.helpers import get_order_date_format

def cart_details(db: Session, user_id: int):

    # 🔹 Get cart IDs
    cart_ids = (
        db.query(GroomingCart.cart_id)
        .filter(GroomingCart.customer_id == user_id)
        .all()
    )

    if not cart_ids:
        return {
            "status": False,
            "message": "cart is empty"
        }

    cart_ids = [c[0] for c in cart_ids]

    # 🔹 Get cart details
    results = (
        db.query(GroomingCartDetails)
        .filter(GroomingCartDetails.cart_id.in_(cart_ids))
        .all()
    )

    cart_details = []
    total_amount = 0

    # 🔹 User primary location
    location_data = (
        db.query(UserLocation)
        .filter(
            UserLocation.user_id == user_id,
            UserLocation.is_primary == 1
        )
        .first()
    )

    latitude = location_data.latitude if location_data else None
    longitude = location_data.longitude if location_data else None
    radius = 100

    for result in results:

        franchise_data = get_nearby_franchise_info(
            db=db,
            franchise_id=result.cart.franchise_id,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
        )

        franchise = franchise_data["franchise"] if franchise_data else None
        distance = franchise_data["distance"] if franchise_data else None

        cart_details.append({
            "franchise_id": franchise.id if franchise else None,
            "franchise_name": "Pet-First",
            "franchise_location": getattr(franchise, "location", None),
            "franchise_city": getattr(franchise, "city", None),
            "franchise_state": getattr(franchise, "state", None),
            "franchise_contact_number": getattr(franchise, "contact_number", None),
            "distance": f"{round(distance, 2)}(kms)" if distance is not None else None,
            "cart_id": result.cart_id,
            "service_id": result.service_id,
            "service_name": result.servicetemp.service_name if result.servicetemp else None,
            "amount": str(result.amount) if result.amount else "0",
            "booking_date": get_order_date_format(result.booking_from),
            "booking_time": result.booking_time
        })

        total_amount += float(result.amount or 0)

    # 🔹 Taxes
    cgst = 0
    sgst = 0
    service_tax = 0

    cgst_comm = total_amount * cgst / 100
    sgst_comm = total_amount * sgst / 100
    service_tax_comm = total_amount * service_tax / 100

    total_service_taxes = cgst_comm + sgst_comm + service_tax_comm

    bill_details = {
        "sub_total": f"{total_amount:.2f}",
        "cgst": f"{cgst_comm:.2f}",
        "sgst": f"{sgst_comm:.2f}",
        "service_tax": f"{service_tax_comm:.2f}",
        "service_fee_taxes": f"{total_service_taxes:.2f}",
        "total_amount": f"{(total_amount + total_service_taxes):.2f}"
    }

    return {
        "status": True,
        "data": cart_details,
        "bill_details": bill_details,
        "message": "cart details info."
    }
