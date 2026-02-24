from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes.customers_auth import router
from app.routes.customers_logout import router as logout_router
from app.routes.customers_profile import router as profile_router
from app.routes.customers_pets_info import router as pet_router
from app.routes.trainers import router as trainer_router
from app.routes.cart import router as cart_router
from app.routes.customers_reunion import router as reunion_router
from app.routes.customers_bank_info import router as bank_router
from app.routes.customers_booking import router as booking_router
from app.routes.get_franchise import router as franchise_router
from app.routes.customers_pet_adoption import router as pet_adoption_router
from app.routes.get_grooming import router as grooming_router
from app.routes.customers_events import router as event_router
from app.routes.customers_review import router as review_router
from app.routes.customers_notify import router as notify_router
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
import app.models

app = FastAPI(title="PetFirst API")

app.state.config = {
    "RECORDS_PER_PAGE": 10
}

# ✅ Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security for API's 
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Pet-First API",
        version="1.0.0",
        description="API with JWT auth",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # 🔐 Only protect specific routes 
    secure_paths = [
        "/api/customer/get-profile",
        "/api/customer/modify-profile-name",
        "/api/customer/update-profile-pic",
        "/api/customer/get-locations",
        "/api/customer/add-primary-location",
        "/api/customer/delete-location/{location_id}",
        "/api/customer/get-pet-parent",
        "/api/customer/add-pet-parent",
        "/api/customer/pet-parent/{pet_parent_id}",
        "/api/customer/pet-parent/{pet_parent_id}/update",
        "/api/customer/pet-parent-delete/{pet_parent_id}",       
        "/api/customer/create-enquiry/{pet_adoption_id}",
        "/api/customer/enquiries-list",
        "/api/customer/get-online-pets-list",
        "/api/customer/pet-adoption-details/{pet_id}",                 
        "/api/customer/get-bank-details",
        "/api/customer/add-bank-details",
        "/api/customer/update-bank-primary/{bank_id}",
        "/api/customer/delete-bank-account/{bank_id}",
        "/api/customer/add-pet",
        "/api/customer/update-pet-pic/{pet_id}",
        "/api/customer/get-pet-details",
        "/api/customer/update-pet/{pet_id}",
        "/api/customer/add-primary-pet",
        "/api/customer/get-pet/{pet_id}",
        "/api/customer/add-user-location/{user_id}",
        "/add-to-cart",
        "/api/customer/get-cart-details",
        "/api/customer/get-bookings",
        "/api/customer/get-booking-details/{booking_id}",
        "/api/customer/cancel-booking",
        "/api/customer/get-upcoming-bookings",
        "/api/customer/create-trainer-booking",
        "/api/customer/reschedule-trainer-booking",
        "/api/customer/add-cart-grooming",
        "/api/customer/get-cart-grooming-details",
        "/api/customer/clear-grooming-cart/{franchise_id}",
        "/api/customer/remove-grooming-service-to-cart/{cart_id}",
        "/api/customer/edit-cart-grooming/{cart_id}",
        "/api/customer/get-events-list",
        "/api/customer/event/{event_id}",
        "/api/customer/event/create-booking/{event_id}",
        "/api/customer/add-franchise-review",
        "/api/customer/add-franchise-doctor-review",
        "/api/customer/add-trainer-review",
        "/api/customer/get-trainer-reviews",
        "/api/customer/get-notify",
        "/api/customer/clear-notify",
        "/api/customers/customer/logout"
        ]

    for path in openapi_schema["paths"]:
        if path in secure_paths:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
        else:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method].pop("security", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(router)
app.include_router(logout_router)
app.include_router(profile_router)
app.include_router(pet_router)
app.include_router(trainer_router)
app.include_router(cart_router)
app.include_router(booking_router)
app.include_router(reunion_router)
app.include_router(bank_router)
app.include_router(franchise_router)
app.include_router(grooming_router)
app.include_router(event_router)
app.include_router(review_router)
app.include_router(notify_router)
app.include_router(pet_adoption_router)
