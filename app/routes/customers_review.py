from fastapi import APIRouter
from app.controllers.customers.Franchises.Reviews.review_controller import add_franchise_review, add_franchise_Doctor_review
from app.controllers.customers.Trainers.trainer_reviews_controller import get_trainer_review, store_trainer_review

router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Add Reviews"]
)

router.post("/add-franchise-review")(add_franchise_review)
router.post("/add-franchise-doctor-review")(add_franchise_Doctor_review)

# Add Trainer Reviews
router.get("/get-trainer-reviews")(get_trainer_review)
router.post("/add-trainer-review")(store_trainer_review)
