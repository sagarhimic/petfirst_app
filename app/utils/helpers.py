from datetime import datetime, date, time
from typing import Optional
from fastapi import HTTPException, Request

def format_date(date_val: Optional[datetime], fmt: str = "%d-%m-%Y") -> Optional[str]:
    """
    :param date_val: datetime object or None
    :param fmt: date format (default: DD-MM-YYYY)
    :return: formatted date string or None
    """
    if not date_val:
        return None
    return date_val.strftime(fmt)

def format_date_db(date_value) -> Optional[str]:
    """
    Laravel equivalent of format_date_db()
    Returns date in YYYY-MM-DD or None
    """
    if date_value in (None, "", []):
        return None

    try:
        return datetime.fromisoformat(str(date_value)).strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(str(date_value), "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

def format_time(value):
    """
    Convert time or datetime to 12-hour formatted time string
    Example: 13:30:00 -> 01:30 PM
    """
    if not value:
        return None

    # If datetime, extract time
    if isinstance(value, datetime):
        value = value.time()

    if isinstance(value, time):
        return value.strftime("%I:%M %p")

    return str(value)

def rating_perc(count: int, total: int) -> int:
    """
    Calculate rating percentage
    Example: count=3, total=10 -> 30
    """
    if not total or total == 0:
        return 0

    return round((count / total) * 100)

def get_order_date_format(value):
    if not value:
        return None

    if isinstance(value, (datetime, date)):
        return value.strftime("%d-%m-%Y")

    return str(value)
    
def parent_types(val: int) -> str:
    options = {
        1: "Father",
        2: "Mother",
        3: "Siblings"
    }
    return options.get(val, "")

def parse_date(value: str | None) -> date | None:
    """
    Accepts: 'YYYY-MM-DD'
    Returns: date object
    """
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format: {value}. Expected YYYY-MM-DD"
        )


def parse_time(value: str | None) -> time | None:
    """
    Accepts: 'HH:MM'
    Returns: time object
    """
    if not value:
        return None

    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid time format: {value}. Expected HH:MM"
        )

def build_full_url(request: Request, path: str | None):
    if not path:
        return None
    return f"{request.base_url}{path.lstrip('/')}"

# def booking_type_price(booking_type: int, kms: float) -> float:
#     if booking_type == 1:      # Tele Medicine
#         return 500
#     elif booking_type == 2:    # House Call
#         return 500 + (kms * 50)
#     return 0

def booking_type_price(booking_type: int, kms: float) -> float:
    if booking_type == 1:
        return {
            "price": 600,
            "hours_diff": 15
        }

    elif booking_type == 2:
        if kms < 5:
            return {
                "price": 1000,
                "hours_diff": 75
            }
        elif 5 <= kms < 7:
            return {
                "price": 1000,
                "hours_diff": 75
            }
        elif 7 <= kms <= 15:
            return {
                "price": 1500,
                "hours_diff": 135
            }
        else:
            return "Not Serviceable"



