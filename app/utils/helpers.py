from datetime import datetime
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
