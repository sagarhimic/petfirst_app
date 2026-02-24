from datetime import datetime, timedelta
from app.utils.helpers import booking_type_price

def generate_time_slots_service(
    booking_type: int,
    kms: float
):
    try:
        booking_details = booking_type_price(booking_type, kms)
        hour_diff = booking_details["hours_diff"]

        start_time = datetime.strptime("10:00 AM", "%I:%M %p")
        end_time = datetime.strptime("11:59 PM", "%I:%M %p")

        time_slots = []
        current = start_time

        while current <= end_time:
            time_slots.append(current.strftime("%I:%M %p").lstrip("0"))
            current += timedelta(minutes=hour_diff)

        slot_types = []

        for slot in time_slots:
            slot_time = datetime.strptime(slot, "%I:%M %p").time()

            if datetime.strptime("10:00 AM", "%I:%M %p").time() <= slot_time < datetime.strptime("12:00 PM", "%I:%M %p").time():
                slot_types.append({
                    "type": "morning",
                    "Time": slot
                })

            elif datetime.strptime("12:00 PM", "%I:%M %p").time() <= slot_time < datetime.strptime("05:00 PM", "%I:%M %p").time():
                slot_types.append({
                    "type": "afternoon",
                    "Time": slot
                })

            elif datetime.strptime("05:00 PM", "%I:%M %p").time() <= slot_time <= datetime.strptime("11:59 PM", "%I:%M %p").time():
                slot_types.append({
                    "type": "evening",
                    "Time": slot
                })

        return {
            "status": 200,
            "slots": slot_types,
            "message": "generated Timeslots."
        }

    except ValueError as ve:
        return {
            "status": False,
            "message": str(ve)
        }
