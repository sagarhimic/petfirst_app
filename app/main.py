from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes.customers_auth import router
from app.routes.customers_logout import router as logout_router
from app.routes.customers_profile import router as profile_router
from app.routes.customers_pets_info import router as pet_router
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PetFirst API")

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
        "/api/customer/add-pet",
        "/api/customer/update-pet-pic/{pet_id}",
        "/api/customer/get-pet-details",
        "/api/customer/update-pet/{pet_id}",
        "/api/customer/add-primary-pet",
        "/get-pet/{pet_id}",
        "/add-user-location/{user_id}",
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
