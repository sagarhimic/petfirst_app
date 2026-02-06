# app/helpers/common.py

def rating_perc(count: int, total: int) -> int:
    if total == 0:
        return 0
    return round((count / total) * 100)


def format_time(time_obj):
    return time_obj.strftime("%I:%M %p") if time_obj else None
