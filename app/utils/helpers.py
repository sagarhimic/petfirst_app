from datetime import datetime, date
from typing import Optional

def format_date(date_val: Optional[datetime], fmt: str = "%d-%m-%Y") -> Optional[str]:
    """
    :param date_val: datetime object or None
    :param fmt: date format (default: DD-MM-YYYY)
    :return: formatted date string or None
    """
    if not date_val:
        return None
    return date_val.strftime(fmt)

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

