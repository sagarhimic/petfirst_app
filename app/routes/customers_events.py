from fastapi import APIRouter
from app.controllers.customers.Franchises.Events.events_controller import get_events_list, show_event, create_event_booking
router = APIRouter(
    prefix="/api/customer",
    tags=["Events & Activities"]
)

router.get("/get-events-list")(get_events_list)
router.get("/event/{event_id}")(show_event)
router.post("/event/create-booking/{event_id}")(create_event_booking)


